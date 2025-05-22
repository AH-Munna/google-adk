from pyautogui import click, moveTo, hotkey, write, position, doubleClick
from time import sleep
from image_automation.components.helper.find_image import find_image
from image_automation.components.helper.play_audio import play_audio

# Define constants for better readability
IMAGE_BASE_PATH = 'image_automation/images/pin_upload/'
CONFIDENCE_THRESHOLD = 0.8

def find_and_click(image_name, x_offset=0, y_offset=0, duration=0.2, base_path=IMAGE_BASE_PATH) -> dict:
    """Helper function to find an image and click on it with optional offsets."""
    full_path = f"{base_path}{image_name}"
    image_loc = find_image(full_path, CONFIDENCE_THRESHOLD)
    
    if image_loc is None:
        return {"success": False, "message": f"{full_path} not found"}
    
    click(image_loc.left + x_offset, image_loc.top + y_offset, duration=duration)
    return {"success": True, "message": f"Clicked on {full_path}"}

def create_new():
    """Create a new Pinterest pin and prepare for image upload."""
    # Click on new pin button
    result = find_and_click('new_pin.png', y_offset=30)
    if not result["success"]:
        return result
    
    # Click on picture upload button
    result = find_and_click('pic_upload.png')
    if not result["success"]:
        return result
    
    # Select image
    result = find_and_click('pic_select_2.png', x_offset=120, y_offset=60)
    if not result["success"]:
        return result
    
    # Delete previous selection and double-click to confirm
    hotkey('delete')
    sleep(0.3)
    doubleClick()
    
    return {"success": True, "message": "New pin created successfully"}

def paste_from_clipboard(field_image, y_offset=0):
    """Helper function to paste content from clipboard to a specific field."""
    result = find_and_click(field_image, x_offset=100, y_offset=50)
    if not result["success"]:
        return result
    
    hotkey('ctrl', 'a')
    hotkey('win', 'v')
    
    clipboard_result = find_and_click('clipboard.png', x_offset=150, y_offset=y_offset, base_path='image_automation/images/')
    return clipboard_result

def paste_texts(board_name, board_pos):
    """Fill in the pin details using clipboard content."""
    # Paste title, description and link from clipboard
    fields_to_paste = [
        ('pin-title.png', 330),
        ('pin-description.png', 250),
        ('pin-link.png', 180)
    ]
    
    for field_image, y_offset in fields_to_paste:
        result = paste_from_clipboard(field_image, y_offset)
        if not result["success"]:
            return result
    
    # Select board
    result = find_and_click('pin-board.png', x_offset=200, y_offset=40)
    if not result["success"]:
        return result
    
    result = find_and_click('pin-search.png', x_offset=200, y_offset=40)
    if not result["success"]:
        return result
    
    # Type board name and select from results
    hotkey('ctrl', 'a')
    write(board_name)
    sleep(0.5)
    
    # Move to board position in dropdown
    current_left, current_top = position()
    moveTo(current_left - 120, current_top + (board_pos * 50), duration=0.2)
    click()
    
    return {"success": True, "message": "Text pasted successfully"}

def pinterest_upload(num_of_images:int=1, board_name:str="", board_pos:int=1):
    """
    Uploads a specified number of images to a Pinterest board.

    Parameters:
    - num_of_images (int): Number of images to upload.
    - board_name (str): Name of the Pinterest board.
    - board_pos (int): Position of the board in the dropdown.
    
    Returns:
    - str: Success or error message.
    """
    # Play audio notification
    # play_audio('image_automation/audio/pinterest_upload_jp.wav')
    
    # Switch to Pinterest tab
    chrome_tab_result = find_and_click('pinterest_chrome.png', base_path='image_automation/images/tabs/')
    if not chrome_tab_result["success"]:
        return chrome_tab_result["message"]
    
    # Upload each image
    for i in range(num_of_images):
        # Create new pin
        create_result = create_new()
        if not create_result["success"]:
            return create_result["message"]
        
        sleep(0.5)
        
        # Fill in details
        paste_result = paste_texts(board_name, board_pos)
        if not paste_result["success"]:
            return paste_result["message"]
        
        print(f"Image {i+1} uploaded")
        sleep(1)
    
    return f'Successfully uploaded {num_of_images} images to board {board_name}.'