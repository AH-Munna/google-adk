from pyautogui import locateOnScreen
from time import sleep
import sys

def find_image(image:str, confidence=0.9, tries=8, no_exit=False, long=False)-> dict[str, int]:
    """
    looks for image on screen
    """
    def try_to_find_image():
        try:
            image_loc = locateOnScreen(image, confidence=confidence)
            print("\033[32mimage found.\033[0m")
            return image_loc
        except:
            if k == tries:
                if no_exit:
                    print("\033[31mImage not found\033[0m")
                    return None
                else:
                    sys.exit("\033[31mImage not found. exiting...\033[0m")
    
    k = 0
    print(f'trying to find ', image, "sleeping for", end=': ')
    while(k < tries):
        sleep_time = (k * 0.5) if not long else (int((tries - k)/3))
        print(sleep_time, end=', ', flush=True)
        sleep(sleep_time)
        k = k + 1

        if image_loc:=try_to_find_image():
            break
    return image_loc
