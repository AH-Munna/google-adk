from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search

instruction = 'content writer agent to help with keyword research, article or content writing.'

description = 'This ai assistant is a content writer agent that can help with keyword research, article generation and content writing. has a google search tool for searching the internet.'

APP_NAME="content_writer_agent"
USER_ID="user1234"
SESSION_ID="1234"

# pyautogui agent.
root_agent = Agent(
    name=APP_NAME,
    # model="gemini-2.0-flash-001",
    model="gemini-2.0-flash-exp",
    description=description,
    instruction=instruction,
    tools=[google_search],
)

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)