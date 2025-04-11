# tk_calculator_agent.py

import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import built_in_code_execution
from google.genai import types

# Constants specific to this agent:
AGENT_NAME = "tkinter_calculator_agent"
APP_NAME = "tk_calculator_app"
USER_ID = "user1234"
SESSION_ID = "session_tkinter_calc"
MODEL = "gemini-2.0-flash-exp"

# Instructions for generating a Tkinter calculator:
instruction_text = """
You are an agent specialized in building UI applications using Python's Tkinter library.
When given a user request to launch a calculator, output fully functional Python code that 
creates a Tkinter window with a working calculator. The calculator should include digits, 
basic arithmetic operators (+, -, *, /), a clear function, and an equal button to compute 
the result. Make sure the code is executable so that calling it will pop up the calculator UI.
"""
instruction_text = """
You are an agent specialized in pyautogui script using Python's pyautogui library.
When given a user request create scripts, output fully functional Python code that 
can do various things designed for pyautogui. Make sure the code is executable.
"""

# Create the agent with the built-in code execution tool.
tk_calculator_agent = LlmAgent(
    name=AGENT_NAME,
    model=MODEL,
    tools=[built_in_code_execution],
    instruction=instruction_text,
    # description="Agent that generates and executes code to launch a Tkinter calculator app."
    description="Agent that generates and executes code to for pyautogui library."
)

# Set up the session and runner.
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=tk_calculator_agent, app_name=APP_NAME, session_service=session_service)

# Define your asynchronous function to interact with the agent.
async def launch_tk_calculator():
    # user_query = "Launch the tkinter calculator app"
    user_query = "create a script using pyautogui to move the mouse to (100, 100) in 5 seconds"
    content = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.executable_code:
                    print("Agent generated code:")
                    print(part.executable_code.code)
                if part.code_execution_result:
                    print("Code Execution Result:", part.code_execution_result.outcome)
        if event.is_final_response():
            print("Final Agent Response:", event.content.parts[0].text)

# Entry point to run the agent.
if __name__ == "__main__":
    try:
        asyncio.run(launch_tk_calculator())
    except Exception as e:
        print("Error executing agent:", e)
