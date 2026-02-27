from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from langchain.chat_models import init_chat_model
from typing import Optional
from typing_extensions import TypedDict

load_dotenv()

model = init_chat_model("google_genai:gemini-2.5-flash-lite")


# --------------------
# State
# --------------------
class State(TypedDict):
    user_query: str
    is_good: Optional[bool]
    llm_output: Optional[str]


# --------------------
# Nodes
# --------------------
def chatbot(state: State):
    response = model.invoke(
        f"Write a short joke about {state['user_query']}. "
        "If it is funny, include the word FUNNY."
    )
    return {
        "llm_output": response.content
    }


def evaluate_joke(state: State):
    """This is the CONDITIONAL node"""
    if "FUNNY" in state["llm_output"]:
        return "good"
    return "bad"


def good_path(state: State):
    return {"is_good": True}


def bad_path(state: State):
    return {"is_good": False}


# --------------------
# Graph
# --------------------
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.add_node("evaluate_joke", evaluate_joke)
graph.add_node("good_path", good_path)
graph.add_node("bad_path", bad_path)

graph.add_edge(START, "chatbot")

# CONDITIONAL EDGES
graph.add_conditional_edges(
    "evaluate_joke",
    evaluate_joke,
    {
        "good": "good_path",
        "bad": "bad_path",
    },
)

graph.add_edge("good_path", END)
graph.add_edge("bad_path", END)

app = graph.compile()
result = app.invoke({"user_query": "give me funny joke"})
print(result)