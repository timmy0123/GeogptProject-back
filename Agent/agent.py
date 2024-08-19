from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint import MemorySaver
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")


def concat(original: list, new: list) -> list:
    return original + new


class ChatState(TypedDict):
    messages: Annotated[list, concat]


class ChatStateGraph:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", temperature=0.5, google_api_key=api_key)
        workflow = StateGraph(ChatState)
        workflow.add_node("chat", self.chat)
        workflow.add_edge("chat", END)
        workflow.set_entry_point("chat")
        self.graph = workflow.compile(checkpointer=MemorySaver())

    def chat(self, state: ChatState) -> ChatState:
        answer = self.llm.invoke(
            state["messages"])
        return {"messages": [answer]}


# config = {"configurable": {"thread_id": "1"}}
# agent = ChatStateGraph()
# count = 0
# while True:
#     user_input = input(">>> ")
#     INIT_PROMPT = """
#                 You are a Geographical Information System (GIS) agent. Your task is to analyze geographical data provided in CSV or GeoJSON format and answer questions related to it.
#                 Your response should consist of two parts:
#                 Answer: A clear and concise response to the User's question.
#                 Geographical Information: Detailed information that can be visualized on a Leaflet map.
#                 Use the following json format for your responses:
#                 {
#                     "messages": ["Your answer here"],
#                     "geodata": [
#                         {
#                         "type": "Marker",
#                         "name": "Marker 1",
#                         "location": [10.0, 10.0],
#                         "description": "This is marker 1"
#                         },
#                         {
#                         "type": "Polygon",
#                         "name": "Polygon 1",
#                         "location": [[10.0, 10.0], [10.0, 20.0], [20.0, 20.0], [20.0, 10.0]],
#                         "description": "This is polygon 1"
#                         },
#                         {
#                         "type": "Polyline",
#                         "name": "Polyline 1",
#                         "location": [[10.0, 10.0], [10.0, 20.0], [20.0, 20.0], [20.0, 10.0]],
#                         "description": "This is polyline 1"
#                         }
#                     ]
#                 }
#                 Marker: Represents a specific point on the map.
#                 Polygon: Represents a closed shape defined by multiple points.
#                 Polyline: Represents a line connecting multiple points.
#                 Make sure your response is formatted in valid JSON.
#             """
#     if count == 0:
#         message = {"messages": [SystemMessage(content=INIT_PROMPT),
#                                 HumanMessage(content=user_input)]}
#     else:
#         message = {"messages": [HumanMessage(content=user_input)]}
#     r = agent.graph.invoke(message, config)
#     print("AI: " + r["messages"][-1].content)
#     count += 1
