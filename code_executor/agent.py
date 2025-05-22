from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from code_executor.components.code_executor import execute_code_from_string
instruction = """\
You are an AI assistant that can execute Python code on the user's local system.
Your primary tool is 'execute_code_from_string'.
When a user asks for a task that can be accomplished with a Python script:
1. Understand the request clearly.
2. Generate a concise, correct, and complete Python code snippet to perform the task.
3. Ensure the code utilizes the available modules (like os, sys, reportlab, pyautogui, etc., as detailed in the tool's description).
4. Pass this code string to the 'execute_code_from_string' tool.
For example, to create a PDF, generate code using 'reportlab'. For GUI automation, use 'pyautogui'.
The code will be run in an environment where common standard libraries and specific third-party libraries are available.\
"""

description = """\
This agent specializes in executing Python code snippets on the local system.
It leverages the 'execute_code_from_string' tool, which has access to modules like
os, sys, json, re, math, pygame, pyautogui, fastapi, and reportlab.
Use this agent for tasks involving file operations, data manipulation, PDF generation,
GUI automation, and other scriptable actions on the local machine.\
"""

APP_NAME="local_code_executor_agent"
USER_ID="user1234"
SESSION_ID="1234"

# pyautogui agent.
root_agent = Agent(
    name=APP_NAME,
    # model="gemini-2.0-flash-001",
    model="gemini-2.5-pro-exp-03-25",
    description=description,
    instruction=instruction,
    tools=[execute_code_from_string],
)


session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)