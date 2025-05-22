from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from simple_tool_agent.components.pdf_generator2 import generate_pdf

instruction = """
generate_pdf: This ai assistant can generate a pdf document.
"""

description = """
This ai assistant can generate a pdf document based on the given list items and a title.
"""

APP_NAME="simple_tool_agent"
USER_ID="user1234"
SESSION_ID="1234"

# pyautogui agent.
root_agent = Agent(
    name=APP_NAME,
    model="gemini-2.5-pro-exp-03-25",
    description=description,
    instruction=instruction,
    tools=[generate_pdf],
)


session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)