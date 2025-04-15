from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from code_executor.code_executor import execute_code_from_string

instruction = """
    It can also execute python code from string.
"""
description = """
I can also execute python code from string that will print the output to console.
"""

APP_NAME="local_code_executor_agent"
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