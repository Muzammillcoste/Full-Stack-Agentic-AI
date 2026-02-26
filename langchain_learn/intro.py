from typing_extensions import Annotated, TypedDict
from langgraph.graph import START, END, add_messages, StateGraph
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model("google_genai:gemini-2.5-flash-lite")


class State(TypedDict):
    message: Annotated[list, add_messages]


def chatbot(state: State):
    response = model.invoke(state["message"])
    return {"message": [response]}


def samplenode(state: State):
    return {"message": [AIMessage(content="sample node added")]}


# build graph
state_graph = StateGraph(State)

state_graph.add_node("chatbot", chatbot)
state_graph.add_node("samplenode", samplenode)

state_graph.add_edge(START, "chatbot")
state_graph.add_edge("chatbot", "samplenode")
state_graph.add_edge("samplenode", END)

compile_graph = state_graph.compile()

# invoke correctly
result = compile_graph.invoke(
    {"message": [HumanMessage(content="Hi, my name is Tony")]}
)

print(result)