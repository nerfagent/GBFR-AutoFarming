import cv2
import concurrent.futures
import easyocr
import keyboard
import numpy as np
import pyautogui
from pynput.keyboard import Controller as Controllerk
from pynput.mouse import Button, Controller as Controllerm
import re
import time

# Get the size of the primary screen
screen_size = pyautogui.size()
print("Primary screen size:", screen_size)

initial_resume = { 'x0' : 0, 'y0': screen_size.height*3//4, 'x1': screen_size.width//4, 'y1': screen_size.height//4 - 50 }
protocol_mode = { 'x0' : 780, 'y0': 170, 'x1': 340, 'y1': 80}
time_left = { 'x0' : 1648, 'y0': 121, 'x1': 136, 'y1': 35}

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# pynput controller
kb = Controllerk()
mouse = Controllerm()

stop_flag = False
repeat_quest_l = False
pause_flag = False # useless
protocol_mode_l = False
time_left_l = 0

def repeat_quest():
    # i = 0
    while not stop_flag:
        # i += 1
        # print("looping")
        global repeat_quest_l
        global time_left_l
        global protocol_mode_l

        screenshot = pyautogui.screenshot(region=(time_left['x0'], time_left['y0'], time_left['x1'], time_left['y1']))
        screenshot_np = np.array(screenshot)
        screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        results = reader.readtext(screenshot_rgb)
        for (bbox, text, prob) in results: # for later if statement for SBA
            match = re.search(r'\d+', text)
            if match:
                temp = int(match.group(0))
                if 30 < temp < 60:
                    time_left_l = temp

        if time_left_l < 50: # for later if statement for SBA
            screenshot = pyautogui.screenshot(region=(protocol_mode['x0'], protocol_mode['y0'], protocol_mode['x1'], protocol_mode['y1']))
            screenshot_np = np.array(screenshot)
            screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
            results = reader.readtext(screenshot_rgb)
            for (bbox, text, prob) in results:
                if 'Protocol' in text:
                    protocol_mode_l = True
                    # print("Protocol mode detected, confirmed.")
                    time.sleep(2)
            protocol_mode_l = False

        # repeat quest
        text0 = False
        text1 = False
        text2 = False
        screenshot = pyautogui.screenshot(region=(initial_resume['x0'], initial_resume['y0'], initial_resume['x1'], initial_resume['y1']))
        screenshot_np = np.array(screenshot)
        screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        results = reader.readtext(screenshot_rgb)
        for (bbox, text, prob) in results:
            if 'Repeat' in text:
                text0 = True
            if 'Cancel' not in text:
                text1 = True
            if 'Quest' in text:
                text2 = True
        if text0 and text1 and text2:
            repeat_quest_l = True
            time.sleep(1)
            kb.press('3')
            time.sleep(0.1)
            kb.release('3') # press 3 to repeat quest
            # print("bottom left repeat quest detected, confirmed.")
        repeat_quest_l = False

        time.sleep(3)

def lancelot():
    while not stop_flag:
        if not repeat_quest_l: # and not pause_flag:
            mouse.press(Button.right) # Unique attack
            mouse.press(Button.middle) # Lock on target
            kb.press('r') # Link attack
            # kb.press('g') # SBA
            time.sleep(0.1)
            mouse.release(Button.right)
            mouse.release(Button.middle)
            kb.release('r')
            # kb.release('g')

            if (time_left_l >= 50) or (protocol_mode_l):
                kb.press('g') # SBA
                time.sleep(0.1)
                kb.release('g')

        time.sleep(0.1)

def stop():
    global stop_flag
    keyboard.wait('p')
    stop_flag = True
    print("Stopping the script...")

def main(usingLancelot):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(repeat_quest)
        if usingLancelot:
            executor.submit(lancelot)
        executor.submit(stop)
        # executor.submit(pause)

if __name__ == "__main__":
    time.sleep(3)  # Allow time to switch to the game window
    main(usingLancelot = True)  # This program only works with Lancelot, so usingLancelot is always True
