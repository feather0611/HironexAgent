from langgraph.graph import StateGraph, END

from .router import route_after_geocoding
from .utils.nodes import geocode_node, weather_node
from .utils.state import AppState


graph = StateGraph(AppState)

graph.add_node("geocode", geocode_node)
graph.add_node("get_weather", weather_node)

graph.set_entry_point("geocode")

graph.add_conditional_edges(source="geocode", path=route_after_geocoding, path_map={
    "get_weather": "get_weather",
    "ask_clarification": END,
    "not_found": END,
    "error": END
})

graph.add_edge("get_weather", END)
weather_agent = graph.compile()