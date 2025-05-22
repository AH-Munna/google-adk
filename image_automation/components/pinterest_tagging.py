from image_automation.components.pinterest_tag_comp.tagging_and_publishing import pinterest_tag_app
from image_automation.components.helper.execution_finished import task_executed

def pinterest_tagging(number_of_pins:int=9) -> dict:
    """
    This function tags and schedules a specified number of pins.
    Args:
        number_of_pins (int): The number of pins to tag. Default is 9.
    Returns:
        dict: A dictionary containing the status and message of the operation.
    """
    # play_audio('audio/tag_pin_options_en.wav')
    
    try:
        print("tagging pins...")
        pinterest_tag_app(post_amount=int(number_of_pins))
        
        task_executed()
        return {
            'status': 'success',
            'message': f"Tagged {number_of_pins} pins successfully!"
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }