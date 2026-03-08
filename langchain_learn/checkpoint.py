from typing_extensions import Annotated, TypedDict
from langgraph.graph import START, END, add_messages, StateGraph
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.mongodb import MongoDBSaver
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


DB_URI = "mongodb://admin:admin@localhost:27017"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:

    builder = StateGraph(State)

    builder.add_node("chatbot", chatbot)
    builder.add_node("sample", samplenode)

    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", "sample")
    builder.add_edge("sample", END)

    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "john"}}

    # STREAM execution
    for event in graph.stream(
        {"message": [HumanMessage(content="what is my name?")]},
        config=config,
        stream_mode="values"
    ):
        event["message"][-1].pretty_print()