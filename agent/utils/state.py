from typing import TypedDict, List, Dict, Any, Optional

class ToolResult(TypedDict):
    pass_status: bool
    result: Optional[List[Dict[str, Any]] | Dict[str, Any]]
    error_message: Optional[str]    

class Action(TypedDict):
    tool: str
    tool_input: Optional[Any]

class AppState(TypedDict):
    user_input: str
    api_keys: Dict[str, str]
    action: Optional[Action]
    geocode_result: Optional[ToolResult]
    weather_result: Optional[ToolResult]
    final_answer: Optional[str]
    error_message: Optional[str]

def create_tool_result(
        pass_status: bool=False,
        result: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None,
        error_message: Optional[str] = None
) -> ToolResult:
    return {
        "pass_status": pass_status,
        "result": result,
        "error_message": error_message,
    }

def create_action(
        tool: str,
        tool_input: Optional[Any] = None
):
    return {
        "tool": tool,
        "tool_input": tool_input,
    }

def create_app_state(
    user_input: str,
    api_keys: Dict[str, str],
    action: Optional[Action] = None,
    geocode_result: Optional[ToolResult]=None,
    weather_result: Optional[ToolResult]=None,
    final_answer: Optional[str]=None,
    error_message: Optional[str]=None,
) -> AppState:
    return {
        "user_input": user_input,
        "api_keys": api_keys,
        "action": action,
        "geocode_result": geocode_result,
        "weather_result": weather_result,
        "final_answer": final_answer,
        "error_message": error_message
    }