import cv2
import numpy as np
from google.adk.agents import Agent
from pyautogui import moveTo, click, typewrite, hotkey

def pyautogui_mouse_move(x: int = 100, y: int = 100) -> dict:
    """
    Moves the mouse cursor to the specified coordinates.
    
    Args:
        x (int): The x-coordinate (0-1919).
        y (int): The y-coordinate (0-1079).
        
    Returns:
        dict: Status report.
    """
    moveTo(x, y, duration=5)
    return {
        "status": "success",
        "report": f"Mouse moved to ({x}, {y}) in 5 seconds.",
    }

def find_icon_coordinates(screenshot_path: str, icon_template_path: str) -> tuple:
    """
    Finds the coordinates (center) of the specified icon in the screenshot.
    
    This function uses template matching via OpenCV:
      1. Loads and converts the images to grayscale.
      2. Uses cv2.matchTemplate to compare the screenshot with the icon template.
      3. Finds the best matching location and computes its center.
    
    Args:
        screenshot_path (str): Path to the screenshot image.
        icon_template_path (str): Path to the icon template image.
        
    Returns:
        tuple: (center_x, center_y) coordinates of the icon.
    """
    # Load the screenshot and convert it to grayscale.
    screenshot = cv2.imread(screenshot_path)
    if screenshot is None:
        raise ValueError("Screenshot not found at the provided path.")
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Load the icon template image in grayscale and get its dimensions.
    icon_template = cv2.imread(icon_template_path, cv2.IMREAD_GRAYSCALE)
    if icon_template is None:
        raise ValueError("Icon template not found at the provided path.")
    w, h = icon_template.shape[::-1]
    
    # Perform template matching.
    result = cv2.matchTemplate(gray_screenshot, icon_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Check if the best match is of sufficient quality.
    if max_val < 0.8:  # Adjust this threshold if needed.
        raise ValueError("Icon not found in the screenshot. Try a higher-quality template or adjust the matching threshold.")
    
    # Calculate the center coordinates of the matched area.
    top_left = max_loc
    center_x = top_left[0] + (w // 2)
    center_y = top_left[1] + (h // 2)
    return center_x, center_y

def locate_icon_and_move(screen_path: str, target_path: str) -> dict:
    """
    Locates the given icon from a screenshot and moves the mouse there.
    
    Args:
        screen_path (str): Path to the screenshot image.
        target_path (str): Path to the target image.
        
    Returns:
        dict: Result from the mouse movement function.
    """
    # Use image recognition to determine the icon's center coordinates.
    x, y = find_icon_coordinates(screen_path, target_path)
    # Move the mouse to the determined location.
    return pyautogui_mouse_move(x, y)

# Configure your agent with both the original mouse moving function and the new locator.
root_agent = Agent(
    name="mouse_control_agent",
    model="gemini-2.0-flash-exp",
    description="Agent to move the mouse to a specific coordinate (e.g., the location of a settings button). (example: screenshot_path = images/screen.png. icon_template_path = images/target.png",
    instruction="I can move your mouse cursor to a specific button after locating it from a screenshot.",
    tools=[pyautogui_mouse_move, locate_icon_and_move],
)
