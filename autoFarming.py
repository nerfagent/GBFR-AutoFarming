import cv2
import easyocr
import time
import numpy as np
import pyautogui
from pynput.keyboard import Controller, Key

# Some loops below may looks redundant, but they are necessary to ensure the script works stably.

# Get the size of the primary screen
screen_size = pyautogui.size()
print("Primary screen size:", screen_size)

initial_resume = { 'x0' : 0, 'y0': screen_size.height*3//4, 'x1': screen_size.width//4, 'y1': screen_size.height//4 - 50 }
ten_resume = { 'x0' : screen_size.width//3, 'y0': screen_size.height//3, 'x1': screen_size.width//3, 'y1': screen_size.height//3 }

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Create a keyboard controller object
keyboard = Controller()

while True:
    # print("new loop")
    repeat_quest_m = 0
    repeat_quest_l = 0

    # repeat quest in after 10 rounds
    for i in range(3):
        # print(f"Checking for repeat quest in middle round {i+1}")
        text0 = False
        text1 = False
        text2 = False
        text3 = False
        screenshot = pyautogui.screenshot(region=(ten_resume['x0'], ten_resume['y0'], ten_resume['x1'], ten_resume['y1']))
        screenshot_np = np.array(screenshot)
        screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        results = reader.readtext(screenshot_rgb)
        for (bbox, text, prob) in results:
            # print(f'>>> {text}')
            if 'Repeat' in text:
                text0 = True
            if 'Continue' in text:
                text1 = True
            if 'Quest' in text:
                text2 = True
            if 'playing' in text:
                text3 = True
        if text0 and text1 and text2 and text3:
            repeat_quest_m += 1
        time.sleep(0.5)

    if repeat_quest_m >= 2:
        keyboard.press(Key.up)
        time.sleep(0.1)
        keyboard.release(Key.up)  # press up to select yes
        time.sleep(0.5)
        keyboard.press(Key.enter)
        time.sleep(0.1)
        keyboard.release(Key.enter) # press enter to confirm
        # print("middle repeat quest detected, confirmed.")
    else:
        # repeat quest in after 1st round
        for i in range(3):
            # print(f"Checking for repeat quest in bottom left round {i+1}")
            text0 = False
            text1 = False
            text2 = False
            screenshot = pyautogui.screenshot(region=(initial_resume['x0'], initial_resume['y0'], initial_resume['x1'], initial_resume['y1']))
            screenshot_np = np.array(screenshot)
            screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
            results = reader.readtext(screenshot_rgb)
            for (bbox, text, prob) in results:
                # print(f'>>> {text}')
                if 'Repeat' in text:
                    text0 = True
                if 'Cancel' not in text:
                    text1 = True
                if 'Quest' in text:
                    text2 = True
            if text0 and text1 and text2:
                repeat_quest_l += 1
            time.sleep(0.5)

        if repeat_quest_l >= 2:
            keyboard.press('3')
            time.sleep(0.1)
            keyboard.release('3') # press 3 to repeat quest
            # print("bottom left repeat quest detected, confirmed.")

    time.sleep(5)