from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


llm = ChatGroq(model='openai/gpt-oss-20b',api_key="your_api_key_here")


class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]




def chat_node(state : ChatState):
    # take user query from state
    messages = state['messages']
    # send to llm
    response = llm.invoke(messages)
    # response store state
    return {'messages':[response]}



graph = StateGraph(ChatState)
checkpointer = MemorySaver()


graph.add_node('chat_node',chat_node)


graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)


