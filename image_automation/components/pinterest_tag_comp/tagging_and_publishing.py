from pyautogui import click, moveTo, hotkey
from time import sleep
import sys
import threading
from tkinter import messagebox
from image_automation.components.helper.find_image import find_image
from image_automation.components.helper.play_audio import play_audio
from image_automation.components.helper.pyscreensize import screenHeight, screenWidth


def select_next_pin():
    # selected_pin_loc = find_image('image_automation/images/pin_upload/pin-selected.png', 0.8)
    # moveTo(selected_pin_loc.left + 50, selected_pin_loc.top + 50)
    moveTo(150, 500)
    click()
    
def copy_tag (tag_num, notepad_loc):
    click(notepad_loc)

    moveTo(18, 85 + (tag_num * 36))

    click(clicks=3)
    hotkey('ctrl', 'c')

def paste_tag (browswer_loc):
    click(browswer_loc)

    tagbox_loc = find_image('image_automation/images/tagbox-warning.png', 0.6)
    click(tagbox_loc.left + 100, tagbox_loc.top - 35)
    hotkey('ctrl', 'a')
    hotkey('ctrl', 'v')

    matched_tags_loc = find_image('image_automation/images/matched-tags.png', 0.6)
    click(matched_tags_loc.left + 50, matched_tags_loc.top + 60)

def publish_post (post_num=1):
    find_image('image_automation/images/tag-completed.png', 0.9)
    sleep(1)
    click(screenWidth-110, 235, duration=1)

    sleep(0.5)
    moveTo((screenWidth/2) + 50, (screenHeight/2) + 150)
    click(duration=0.5)
    print("Published post " + str(post_num))
    select_next_pin()

# code starto
def pinterest_tag_app(post_amount):
    try:
        # play_audio('image_automation/audio/tag_pin_start_jp_01.wav')
        # play_audio('image_automation/audio/tag_pin_start_jp_02.wav')
        browser_loc = find_image('image_automation/images/tabs/pinterest_chrome.png', 0.8)
        notepad_loc = find_image('image_automation/images/tabs/notepad.png', 0.9)
        for pin_num in range(post_amount):
            sleep(2)
            for i in range(9):
                sleep(0.2)
                copy_tag(i, notepad_loc)
                paste_tag(browser_loc)
            publish_post(pin_num + 1)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")