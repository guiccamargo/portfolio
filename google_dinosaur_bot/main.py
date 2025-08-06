import time

import pyautogui
from PIL import ImageGrab
from selenium import webdriver


def is_collision(data, x: int, y: int, threshold: int) -> bool:
    """
    Check for obstacles
    :param data: PixelAccess: Color of the pixels on the screenshot
    :param x: horizontal value of the pixel to be checked
    :param y: vertical value of the pixel to be checked
    :param threshold: Color of the obstacle
    :return: return True if the pixel represents an obstacle.
    """
    return data[x, y] < threshold


def play_dino_game():
    """
    Automate Google Dinosaur Gameplay
    """
    # Region where the game is displayed
    game_region = (0, 450, 1280, 750)
    # x distance to check for obstacles
    jump_distance_x = 200
    duck_distance_x = 180
    # y distance to check for ground obstacles
    jump_distance_y = 185
    # y distance to check for aerial obstacles
    duck_distance_y = 140
    # Color code to detect obstacles
    obstacle_color_threshold = 250

    # Wait for the game to be loaded
    time.sleep(3)
    # Start game
    pyautogui.press("up")

    while True:
        # Screenshot of the game region
        screenshot = ImageGrab.grab(bbox=game_region).convert('L')  # Convert image to greyscale for easier analysis
        pixels = screenshot.load()
        # Check for ground obstacles
        if is_collision(pixels, jump_distance_x, jump_distance_y, obstacle_color_threshold):
            pyautogui.press("up")
        # Check for aerial obstacles
        elif is_collision(pixels, duck_distance_x, duck_distance_y, obstacle_color_threshold):
            pyautogui.press('down')
        # Break this loop when the browser is closed
        if len(driver.window_handles) == 0:
            break


# Open the game
driver = webdriver.Firefox()
driver.get("https://elgoog.im/t-rex")
# Start Bot
play_dino_game()
