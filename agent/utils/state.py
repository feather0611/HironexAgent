from typing import TypedDict, List, Dict, Any, Optional

class AppState(TypedDict):
    user_input: str
    api_keys: Dict[str, str]
    choices: Optional[List[Dict[str, Any]]]
    final_answer: Optional[str]
    error_message: Optional[str]