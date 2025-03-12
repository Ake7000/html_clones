import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def poza_screenshot(file_path, screenshot_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options = chrome_options)
    driver.get("file://" + os.path.abspath(file_path))
    time.sleep(2)
    driver.save_screenshot(screenshot_path)
    driver.quit()