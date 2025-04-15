from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

instruction = """
    Agent to answer questions using Google Search.
    It can also help with AI agent development and python programming.
"""
description = """
    I can help with AI agent development and python programming. I can answer your questions by searching the internet. Just ask me agent development or python programming related queries!
"""

APP_NAME="information_and_coding_agent"
USER_ID="user1234"
SESSION_ID="1234"

# pyautogui agent.
root_agent = Agent(
    name=APP_NAME,
    model="gemini-2.0-flash-001",
    description=description,
    instruction=instruction,
    tools=[google_search],
)


session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)