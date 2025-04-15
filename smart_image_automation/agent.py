from google.adk.agents import Agent
from smart_image_automation.components.create_image import create_image  
from smart_image_automation.components.pinterest_upload_settings import image_upload_pinterest
from smart_image_automation.components.upload_to_canva import image_upload_canva

instruction = """
    create_image: Creates a pin image using AI prompt generation and image creation AI.
    image_upload_pinterest: Upload image(s) to Pinterest.
    image_upload_canva: Upload image(s) to Canva.
"""
description = """
    This agent creates pin image using AI prompt generation and image creation AI.
    It also uploads images to Pinterest and Canva.
"""

# pyautogui agent.
root_agent = Agent(
    name="smart_image_automation_agent",
    model="gemini-2.0-flash-001",
    description=description,
    instruction=instruction,
    tools=[create_image, image_upload_pinterest, image_upload_canva],
)