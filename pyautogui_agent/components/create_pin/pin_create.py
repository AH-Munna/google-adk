from helper.groq_api import groq_title_divider, groq_prompt_gen
from pyautogui import click, moveTo, hotkey, hotkey, position
from time import sleep
import sys
from helper.find_image import find_image
from pyperclip import copy, paste

def regen_fail_check():
    if faile_regen_loc:=find_image('images/create_pin/deepseek_failed.png', 0.6, 2):
        moveTo(faile_regen_loc.left + 50, faile_regen_loc.top + 50, duration=1)
        sys.exit("Deepseek failed to generate")

def deepseek_paste_and_copy():
    previos_title_edit_loc = find_image('images/create_pin/previous_title_edit.png', 0.6)
    click(previos_title_edit_loc.left + 120, previos_title_edit_loc.top + 40, duration=1)

    x, y = position()
    moveTo(x + 100, y, duration=0.5)
    hotkey('ctrl', 'a')
    hotkey('ctrl', 'v')

    click(find_image('images/create_pin/send_button.png', 0.6), duration=1)
    moveTo(200, 200, 5)

    copy_loc = find_image('images/create_pin/deepseek_copy_regen.png', 0.6, 30)
    click(copy_loc.left + 15, copy_loc.top + 20, duration=1)

def title_prepare():
    click(find_image('images/create_pin/title_dividing.png', 0.9), duration=1)

    previos_title_loc = find_image('images/create_pin/previous_title.png', 0.6)
    click(previos_title_loc.left + 500, previos_title_loc.top + 100, duration=1)

    deepseek_paste_and_copy()

def prompt_create():
    click(find_image('images/create_pin/image_prompt.png', 0.7), duration=1)

    previous_prompt_loc = find_image('images/create_pin/previous_prompt.png', 0.7)
    moveTo(previous_prompt_loc.left + 500, previous_prompt_loc.top + 110, duration=1)

    deepseek_paste_and_copy()

def image_create():
    click(find_image('images/tabs/ideogram.png', 0.7), duration=0.5)

    generate_button_loc = find_image('images/create_pin/ideogram_generate_button.png', 0.6)
    moveTo(generate_button_loc.left - 500, generate_button_loc.top + 15, duration=0.5)
    click(duration=0.5)
    sleep(0.5)
    hotkey('ctrl', 'a')
    sleep(0.5)
    hotkey('ctrl', 'v')
    sleep(1)
    click(find_image('images/create_pin/ideogram_generate_button.png', 0.6), duration=2)

def pin_create(type_of_execution=1, thinking_model='y', browser_tab='season', title=None):
    try:
        if type_of_execution == 1:
            if not title:
                title = paste()
            copy(groq_prompt_gen(groq_title_divider(title, thinking_model == 'y'), thinking_model == 'y'))
            sleep(1)
            print("\033[32mPrompt generated.\033[0m")
            # play_audio('audio/generate_image_en.wav')
            sleep(1)
            print("\033[32mTrying to generate image...\033[0m")
            sleep(1)
            if browser_tab == 'season':
                click(find_image('images/tabs/seasoninspired_chrome.png', 0.8), duration=1)
            else:
                click(find_image('images/tabs/red_chrome.png', 0.8), duration=1)
        elif type_of_execution == 2:  # Not managed, keeping original logic
            click(find_image('images/tabs/seasoninspired_chrome.png', 0.7), duration=0.5)
            click(find_image('images/tabs/deepseek.png', 0.7), duration=1)
            title_prepare()
            prompt_create()
        else:
            print("\033[31mPlease choose between 1 and 2\033[0m")
            return  # In GUI, this won't recurse since input is controlled
        
        image_create()
    except ValueError:
        print("\033[31mInvalid input\033[0m")