from image_automation.components.upload_to_canva_comp.upload_settings import upload_to_canva_settings


def image_upload_canva(number_of_image:int=10, downloaded_image_pos:int=0) -> dict:
    """
    uploads specified number of images to Canva.
    Args:
        number_of_image (int): The number of images to upload. optional. default is 10.
        downloaded_image_pos (int): The position of the downloaded image. optional. default is 0.
    Returns:
        dict: A dictionary containing the status and message of the upload process.
    """

    try:
        upload_to_canva_settings(number_of_image=number_of_image, downloaded_image_pos=downloaded_image_pos)
        return {
            "status": "success",
            "message": f"Successfully uploaded {number_of_image} images to Canva.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred while uploading images to Canva: {str(e)}",
        }