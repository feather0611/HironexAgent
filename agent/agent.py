from langgraph.graph import StateGraph

from .utils.nodes import geocode_node
from .utils.state import AppState


graph = StateGraph(AppState)

graph.add_node("geocode", geocode_node)
graph.add_node("get_weather", weather_node)
# app = graph.compile()