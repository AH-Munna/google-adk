import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import built_in_code_execution
from google.genai import types

AGENT_NAME = "mouse_control_agent"
APP_NAME = "mouse_control"
USER_ID = "user1234"
SESSION_ID = "session_code_exec"

# Define the agent
mouse_agent = LlmAgent(
    name=AGENT_NAME,
    model="gemini-2.0-flash-exp",
    tools=[built_in_code_execution],
    instruction="You can execute Python scripts to control the mouse cursor.",
    description="Executes Python code to move the mouse cursor."
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=mouse_agent, app_name=APP_NAME, session_service=session_service)

async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            print("Agent Response:", event.content.parts[0].text)

# Example script to move the mouse
script = """
move the mouse to (100, 100) in 5 seconds
"""
if __name__ == "__main__":
    try:
        asyncio.run(call_agent_async(script))
    except Exception as e:
        print("Error executing agent:", e)
