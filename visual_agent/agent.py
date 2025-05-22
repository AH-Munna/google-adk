from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from code_executor.components.code_executor import execute_code_from_string

instruction = """
this agent can write codes and then executes it to interact with the screen.
    execute_code_from_string: It can execute python code from string.
"""
description = """
it generates codes that finds coordinate of presaved images on the screen and interacts with it.
This agent can execute python code from string which will run on local system.

presaved images:
    1. vs code icon: image_automation/images/tabs/vs_code.png
"""

APP_NAME="pyautogui_agent"
USER_ID="user1234"
SESSION_ID="1234"

# pyautogui agent.
root_agent = Agent(
    name=APP_NAME,
    model="gemini-2.0-flash-001",
    description=description,
    instruction=instruction,
    tools=[execute_code_from_string],
)


session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)