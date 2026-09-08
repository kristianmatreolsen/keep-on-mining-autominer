import pyautogui
import keyboard
import math
import os
import sys
import time
import threading
from PIL import Image, ImageChops

pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0.01

running = False

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
# Approximate corners of the diamond-shaped game board as screen proportions.
BOARD_CORNERS = (
    (0.54, 0.18),  # top
    (0.80, 0.38),  # right
    (0.50, 0.68),  # bottom
    (0.18, 0.38),  # left
)
EDGE_SECONDS = 2.0

resource_directory = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
template_image = Image.open(os.path.join(resource_directory, "keep_on_mining.png")).convert("RGB")
white_background = Image.new("RGB", template_image.size, "white")
button_bounds = ImageChops.difference(template_image, white_background).getbbox()
button_template = template_image.crop(button_bounds) if button_bounds else template_image

def find_artifact_button():
    region_left = round(SCREEN_WIDTH * 0.30)
    region_top = round(SCREEN_HEIGHT * 0.66)
    region_width = round(SCREEN_WIDTH * 0.40)
    region_height = round(SCREEN_HEIGHT * 0.25)
    screenshot = pyautogui.screenshot(region=(region_left, region_top, region_width, region_height)).convert("RGB")

    yellow_pixels = []
    minimum_run = max(60, round(SCREEN_WIDTH * 0.08))
    for y in range(region_height):
        run_start = None
        for x in range(region_width + 1):
            is_yellow = (
                x < region_width
                and screenshot.getpixel((x, y))[0] >= 220
                and screenshot.getpixel((x, y))[1] >= 150
                and screenshot.getpixel((x, y))[2] <= 110
            )
            if is_yellow and run_start is None:
                run_start = x
            elif not is_yellow and run_start is not None:
                if x - run_start >= minimum_run:
                    yellow_pixels.append((run_start, x - 1, y))
                run_start = None

    if not yellow_pixels:
        return None

    left = min(run[0] for run in yellow_pixels)
    right = max(run[1] for run in yellow_pixels)
    top = min(run[2] for run in yellow_pixels)
    bottom = max(run[2] for run in yellow_pixels)
    width = right - left + 1
    height = bottom - top + 1
    if not (SCREEN_WIDTH * 0.12 <= width <= SCREEN_WIDTH * 0.30):
        return None
    if not (SCREEN_HEIGHT * 0.06 <= height <= SCREEN_HEIGHT * 0.16):
        return None
    if width / height < 1.5:
        return None

    return region_left + (left + right) // 2, region_top + (top + bottom) // 2

def mine():
    global running

    last_click = 0.0
    circle_started = time.monotonic()
    click_interval = 0.20
    time.sleep(0.3)

    while running:
        elapsed = (time.monotonic() - circle_started) % (4 * EDGE_SECONDS)
        edge_index = int(elapsed // EDGE_SECONDS)
        edge_progress = (elapsed % EDGE_SECONDS) / EDGE_SECONDS
        start_x, start_y = BOARD_CORNERS[edge_index]
        end_x, end_y = BOARD_CORNERS[(edge_index + 1) % len(BOARD_CORNERS)]
        x = round((start_x + (end_x - start_x) * edge_progress) * SCREEN_WIDTH)
        y = round((start_y + (end_y - start_y) * edge_progress) * SCREEN_HEIGHT)

        pyautogui.moveTo(x, y, duration=0)

        current_time = time.monotonic()
        if current_time - last_click >= click_interval:
            pyautogui.click()
            last_click = current_time

        time.sleep(0.03)

def keep_mining():
    global running

    while running:
        try:
            # Keep this slow screen search out of the mining movement loop.
            button = pyautogui.locateCenterOnScreen(
                button_template,
                confidence=0.7,
                grayscale=True
            )

            if button:
                print("KEEP ON MINING found")
                pyautogui.click(button)
                time.sleep(0.25)
                continue

            artifact_button = find_artifact_button()
            if artifact_button:
                print("Artifact popup found")
                pyautogui.click(artifact_button)
                time.sleep(0.5)
            else:
                time.sleep(0.5)
        except Exception as error:
            print(f"Button detection error: {error}")
            time.sleep(0.5)

def start():
    global running

    if not running:
        running = True
        threading.Thread(target=mine, daemon=True).start()
        threading.Thread(target=keep_mining, daemon=True).start()
        print("Started")

def stop():
    global running
    running = False
    print("Stopped")

keyboard.add_hotkey('F8', start)
keyboard.add_hotkey('F9', stop)

print("F8 = Start")
print("F9 = Stop")
print("ESC = Exit")

keyboard.wait('esc')