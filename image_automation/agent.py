from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from image_automation.components.create_image import create_image  
from image_automation.components.pinterest_upload_settings import image_upload_pinterest
from image_automation.components.upload_to_canva import image_upload_canva
from image_automation.components.pinterest_tagging import pinterest_tagging
from image_automation.components.analyze_image import analyze_image

instruction = """
    create_image: Creates a image using AI prompt generation and image creation AI.
    image_upload_canva: Upload image(s) to Canva.
    image_upload_pinterest: Upload image(s) to Pinterest.
    pinterest_tagging: Tags and schedules a specified number of pins.
    analyze_image: Analyzes an image.
"""
description = """
    This agent creates image using AI prompt generation and image creation AI.
    It also uploads images to Canva and Pinterest. This agent can also tag and schedule a specified number of pins.
    it can analyze a given image.
    The agent is designed to automate the process of creating and uploading images to various platforms.
"""

APP_NAME="image_automation_agent"
USER_ID="user1234"
SESSION_ID="1234"

# pyautogui agent.
root_agent = Agent(
    name=APP_NAME,
    model="gemini-2.0-flash-001",
    # model="gemini-2.0-flash-exp",
    description=description,
    instruction=instruction,
    tools=[create_image, image_upload_canva, image_upload_pinterest, pinterest_tagging],
)

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)