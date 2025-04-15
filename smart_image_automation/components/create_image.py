from smart_image_automation.components.create_pin_comp.pin_create import pin_create
from typing import Literal, Union, Optional, Dict
from smart_image_automation.components.helper.play_audio import play_audio

def create_image(
    type_of_execution: Literal["api", "web"] = "api",
    thinking_model: Literal["y", "n"] = "y",
    browser_tab: Literal["season", "red", 'midgeos'] = "midgeos",
    title: Optional[str] = None,
) -> Dict:
    """
    Creates an image using AI prompt generation and image creation in txt-to-img AI. all parameters are optional.
    Args:
        type_of_execution (str): Type of execution, either "api" or "web".
        thinking_model (str): Thinking model, either "y" or "n".
        browser_tab (str): Browser tab, either "season" or "red" or 'midgeos'.
        title (str, optional): Title for the image.
    """

    play_audio('pyautogui_agent/audio/create_image_start_en.wav')

    return pin_create(
        type_of_execution=type_of_execution,
        thinking_model=thinking_model,
        browser_tab=browser_tab,
        title=title
    )