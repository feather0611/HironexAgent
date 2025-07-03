import logging
import os
import sys

from dotenv import load_dotenv

from agent.agent import weather_agent
from agent.utils.state import create_app_state


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S %p'
    )

    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

if __name__ == "__main__":
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    load_dotenv()
    
    api_keys = {
        "google_map_api_key": os.getenv("GOOGLE_MAPS_API_KEY"),
        "owm_api_key": os.getenv("OWM_API_KEY"),
    }
    
    if not api_keys["google_map_api_key"] or not api_keys["owm_api_key"]:
        logger.error("Google Maps API key or OWM API key not found.")
        sys.exit(1)
    
    logger.info("Application started.")
    
    while True:
        user_input = input("Please input the place you want to query:").strip()
        if user_input == "exit":
            break
        if not user_input:
            continue
            
        app_state = create_app_state(user_input, api_keys)
        
        final_state = weather_agent.invoke(app_state)
        
        responses = final_state.get("weather", final_state.get("error_message", "I got nothing."))
        print(responses)
        
        