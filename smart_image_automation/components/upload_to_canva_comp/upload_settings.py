from pyautogui import click, moveTo, hotkey, hotkey, position, dragTo, rightClick, scroll
from smart_image_automation.components.helper.play_audio import play_audio
from time import sleep
import sys
from smart_image_automation.components.helper.find_image import find_image
from smart_image_automation.components.helper.pyscreensize import screenHeight
from threading import Thread
from smart_image_automation.components.helper.constants_vars import IMAGES_BASE_PATH

def upload_to_canva_settings(number_of_image=4, downloaded_image_pos=0):
    Thread(target=play_audio, args=(f'pyautogui_agent/audio/upload_to_canva_en.wav',), daemon=True).start()

    # setup tabs
    if number_of_image != 4:
        click(find_image(f'{IMAGES_BASE_PATH}tabs/seasoninspired_chrome.png', 0.8), duration=0.5)

    click(find_image(f'{IMAGES_BASE_PATH}/tabs/canva.png', 0.9), duration=0.5)
    download_files = find_image(f'{IMAGES_BASE_PATH}/tabs/downloads_folder.png', 0.8)
    click(download_files, duration=0.5)

    # move to files
    todays_downloads = find_image(f'{IMAGES_BASE_PATH}/pin_upload/pic_select_2.png', 0.7)
    moveTo((todays_downloads.left + 52) + (downloaded_image_pos * 108), todays_downloads.top + 50, duration=0.3)

    # select files and paste to canva
    x, y = position()
    dragTo(x+ (number_of_image * 105), y + 30, duration=1)

    canva_controls = find_image(f'{IMAGES_BASE_PATH}/canva/canva_control.png', 0.9)
    dragTo(canva_controls.left + 100, canva_controls.top + 100, duration=1.5)
    sleep(number_of_image/1.6)

    # # clone images
    for i in range (number_of_image-1):
        click(canva_controls.left + 358, canva_controls.top + 15, duration=number_of_image/8)

    moveTo(canva_controls.left + 200, canva_controls.top + 400, duration=0.2)

    # organize canva
    for i in range (number_of_image):
        for j in range (number_of_image):
            if i == j:
                rightClick()
                def set_as_background():
                    click(find_image(f"{IMAGES_BASE_PATH}canva/set_as_backgroung.png", 0.9), duration=0.2)

                    if i == 0 and find_image(f"{IMAGES_BASE_PATH}canva/set_as_backgroung.png", 0.9, 2, True) is not None:
                        return set_as_background()
                set_as_background()

            else:
                click(canva_controls.left + 200, canva_controls.top + 450, duration=0.2)
                hotkey('delete')
        if i != number_of_image-1:
            moveTo(canva_controls.left + 200, canva_controls.top + 450, duration=0.2)
            scroll(screenHeight-40)

    # delete uploaded images
    click(download_files, duration=0.2)
    hotkey('delete')