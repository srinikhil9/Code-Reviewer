import asyncio
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver


# -----------------------------
# Tools
# -----------------------------

@tool("execute_code", return_direct=False)
def execute_code(code: str) -> str:
    """Safely execute minimal Python code and return a result string.

    The tool evaluates code in a restricted environment and returns the value
    of a variable named `result` if present; otherwise a short message.
    """
    safe_globals: Dict[str, Any] = {"__builtins__": {}}
    safe_locals: Dict[str, Any] = {}
    try:
        exec(code, safe_globals, safe_locals)
        if "result" in safe_locals:
            return str(safe_locals["result"])
        return "No result variable defined."
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"


# -----------------------------
# State
# -----------------------------

@dataclass
class FlowState:
    user_input: str
    generated_code: Optional[str] = None
    reviewer_feedback: Optional[str] = None
    docs_code: Optional[str] = None
    orchestrator_decision: Optional[str] = None
    approval_status: Optional[str] = None


# -----------------------------
# LLM helpers
# -----------------------------

def llm(model: str = os.getenv("OPENAI_MODEL", "gpt-4o"), temperature: float = 0.1) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)


async def call_llm(system_prompt: str, user_text: str, model: Optional[str] = None) -> str:
    chain = (ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{q}")]) | llm(model))
    msg = await chain.ainvoke({"q": user_text})
    return msg.content if hasattr(msg, "content") else str(msg)


# -----------------------------
# Orchestrator + Router
# -----------------------------

ORCHESTRATOR_PROMPT = (
    "You are an orchestrator. Decide which agent to call based on the task:\n"
    "- If the task is \"write code\" or \"generate\", respond with GENERATE.\n"
    "- If the task is \"review\" or \"debug\", respond with REVIEW.\n"
    "- If the task is \"add docs\" or \"explain\", respond with DOCUMENT.\n"
    "Respond ONLY with GENERATE, REVIEW, or DOCUMENT."
)


async def orchestrator_node(state: FlowState) -> FlowState:
    decision = await call_llm(ORCHESTRATOR_PROMPT, state.user_input)
    state.orchestrator_decision = decision.strip().upper()
    return state


def router(state: FlowState) -> str:
    decision = (state.orchestrator_decision or "").upper()
    if decision == "GENERATE":
        return "code_generator"
    if decision == "REVIEW":
        return "code_reviewer"
    if decision == "DOCUMENT":
        return "documentation_agent"
    return "fallback_agent"


# -----------------------------
# Agents
# -----------------------------

GENERATOR_PROMPT = (
    "Write clean, efficient code for: {user_input}.\n"
    "Return ONLY the code, no explanations."
)

REVIEWER_PROMPT = (
    "Review this code for errors, inefficiencies, or security flaws:\n{generated_code}\n"
    "Suggest concise fixes and improvements."
)

DOCS_PROMPT = (
    "Add detailed comments and a docstring to this code:\n{generated_code}\n"
    "Return the code with inline comments."
)


async def code_generator(state: FlowState) -> FlowState:
    system = GENERATOR_PROMPT.format(user_input=state.user_input)
    code = await call_llm(system, state.user_input)
    state.generated_code = code.strip()
    return state


async def code_reviewer(state: FlowState) -> FlowState:
    code = state.generated_code or ""
    system = REVIEWER_PROMPT.format(generated_code=code)
    feedback = await call_llm(system, "Review the code above")
    state.reviewer_feedback = feedback.strip()
    return state


async def documentation_agent(state: FlowState) -> FlowState:
    code = state.generated_code or ""
    system = DOCS_PROMPT.format(generated_code=code)
    documented = await call_llm(system, "Document the code")
    state.docs_code = documented.strip()
    return state


async def fallback_agent(state: FlowState) -> FlowState:
    # Helpful generic assistant behavior
    generic = await call_llm(
        "You are a helpful coding assistant.",
        f"Task: {state.user_input}",
    )
    state.docs_code = generic.strip()
    return state


# -----------------------------
# Feedback loop + human-in-the-loop
# -----------------------------

def needs_retry(state: FlowState) -> bool:
    fb = (state.reviewer_feedback or "").lower()
    return ("error" in fb) or ("fix" in fb)


async def human_in_the_loop(state: FlowState) -> FlowState:
    # Non-interactive default; set env ALLOW_HUMAN_INPUT=1 for console prompt
    if os.getenv("ALLOW_HUMAN_INPUT") == "1":
        try:
            print("Awaiting human approval for generated code... (y/N)")
            ans = input().strip().lower()  # noqa: PLW1514
            state.approval_status = "approved" if ans == "y" else "not approved"
        except Exception:
            state.approval_status = "not approved"
    else:
        state.approval_status = "approved"
    return state


# -----------------------------
# Graph builder
# -----------------------------

def build_graph() -> StateGraph:
    graph = StateGraph(FlowState)

    # Nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("code_generator", code_generator)
    graph.add_node("code_reviewer", code_reviewer)
    graph.add_node("documentation_agent", documentation_agent)
    graph.add_node("fallback_agent", fallback_agent)
    graph.add_node("human_gate", human_in_the_loop)

    # Entry
    graph.set_entry_point("orchestrator")

    # Route
    graph.add_conditional_edges("orchestrator", router, {
        "code_generator": "code_generator",
        "code_reviewer": "code_reviewer",
        "documentation_agent": "documentation_agent",
        "fallback_agent": "fallback_agent",
    })

    # Generator → Reviewer
    graph.add_edge("code_generator", "code_reviewer")

    # Reviewer → Feedback loop or Docs
    def reviewer_route(state: FlowState) -> str:
        return "code_generator" if needs_retry(state) else "documentation_agent"

    graph.add_conditional_edges("code_reviewer", reviewer_route, {
        "code_generator": "code_generator",
        "documentation_agent": "documentation_agent",
    })

    # Docs → Human gate → END
    graph.add_edge("documentation_agent", "human_gate")
    graph.add_edge("human_gate", END)

    # Fallback → END
    graph.add_edge("fallback_agent", END)

    return graph


async def arun(user_input: str) -> Dict[str, Any]:
    memory = MemorySaver()
    graph = build_graph().compile(checkpointer=memory)
    initial = FlowState(user_input=user_input)
    state: FlowState = await graph.ainvoke(initial)
    return {
        "decision": state.orchestrator_decision,
        "generated_code": state.generated_code,
        "reviewer_feedback": state.reviewer_feedback,
        "documented_code": state.docs_code,
        "approval_status": state.approval_status,
    }


def run(user_input: str) -> Dict[str, Any]:
    return asyncio.run(arun(user_input))


if __name__ == "__main__":
    import json
    load_dotenv()
    query = os.environ.get("TASK", "Create a Python function to validate email addresses using regex")
    out = run(query)
    print(json.dumps(out, indent=2))


