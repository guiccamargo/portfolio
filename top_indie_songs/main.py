from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# URL for the playlist
URL = "https://soundcloud.com/buzzing-playlists/sets/buzzing-indie"


def scrap_content() -> tuple[List[dict[str: str]], str]:
    """
    Scrap data from soundcloud Website
    :return: tuple with a list of tracks in the first position, and the date of last update in the second position
    """
    # Create driver
    driver = webdriver.Firefox()
    # Get URL
    driver.get(URL)
    # Wait for the buttons to be clickable
    wait = WebDriverWait(driver, timeout=2)
    # Click accept cookies button
    wait.until(ec.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
    # Click the login widget closing button
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "modal__closeButton"))).click()
    # Wait 15 seconds until all elements to be loaded
    driver.implicitly_wait(15)
    # Get date from last update
    last_update = driver.find_element(By.CLASS_NAME, "relativeTime").get_attribute("datetime")
    # Find all tracks in the playlist
    tracks = driver.find_elements(By.CLASS_NAME, "trackItem")
    # Create a list to store track data
    top_tracks = []
    # Create dicts to store track info
    for track in tracks:
        top_tracks.append({"id": track.find_element(By.CLASS_NAME, "trackItem__number").text,
                           "title": track.find_element(By.CLASS_NAME, "trackItem__trackTitle").text,
                           "artist": track.find_element(By.CLASS_NAME, "trackItem__username").text, })
    # Close driver
    driver.quit()

    return top_tracks, last_update


def show_tracks(tracklist: List[dict[str: str]], current_time: str) -> None:
    """
    Format and print scrapped data
    :param tracklist: List of all tracks as dicts
    :param current_time: String containing last update datetime
    :return: None.
    """
    print("-" * 30)
    print("Most popular indie songs".title())
    print(f"Updated in {current_time.split('T')[0]}\n")
    for track in tracklist:
        print(f"{track['id']} SONG: {track['title']} BY {track['artist']}")


# Execute
show_tracks(*scrap_content())
