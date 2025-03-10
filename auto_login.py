# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009D7559370DDF4E1E3A625397F4E31D26A4DA66CACE946ADF4DF21E4A0D648F2CE1C1FB7E3BF0A6E34B863FFA00550390980DB305645EEB78EE994BCB3032313693F0A6445A9405AA9E78AC446FDDF6F6FE307C6849FD4BC12EA760BE5976282288A7C683186C2EAE754599CB3861A56E84423F31418DC2E572007A7FC075F3355AD44601FE0E79CE79F417E49D832B8EAA8EE0153D74D0C356D92B1A98DF6B481773A1A93F194C78EB95DDCAEBC064E45AD767D77FE12E7ADB04CE5D807F2A22D1F9A791E1E250C9067F98648B5C4BD2A58650ADC1F8DD24946EE86B00396647C6112193399E17F2C0F9F4A55BEE3803D6E2A9BB4FCD2D22FA8B2A8AB7EFFC382862B22F7284516AB7A5B981FE32EDDD9E10882D11749EEB835B8E009DBC1CCF2BFC498FA418FC21747C23B8AD320149DCCB40E95D2A5503AED2F99AA8C929097F6DB986A6C7A96590E3B6B84ADB383768FE34BBDC4D5152F285AA0091856E53"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
