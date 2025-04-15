from typing import Dict
from smart_image_automation.components.pin_upload_comp.pinterest_upload_comp import pinterest_upload
from smart_image_automation.components.helper.execution_finished import task_executed

def image_upload_pinterest(num_of_image:int=1, board_name:str="", board_pos:int=1) -> Dict:
    """
    Upload specified number of image to Pinterest.
    Args:
        num_of_image (int): The number of images to upload. optional. default is 1.
        board_name (str): The name of the Pinterest board.
        board_pos (int): The position of the board. optional. default is 1.
    """

    report = pinterest_upload(board_name=board_name, num_of_images=num_of_image, board_pos=board_pos)
    task_executed()
    return {
    "status": "success",
    "report": report,
}