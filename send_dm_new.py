import os
import sys
import json
import random
import glob
import logging
import pyautogui
from time import sleep
from random import randint, choice
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


COMMENT_COUNT = 25  # This count stands for your rotation count
DELAY = 1

logging.basicConfig(
    level=logging.INFO,
    filename="LogFile.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def get_driver():
    options = Options()
    # options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")
    options.add_argument("start-maximized")
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = Chrome(service=Service(CM().install()), options=options)
    driver.implicitly_wait(DELAY)
    driver.maximize_window()

    return driver


def get_users():
    with open("accounts.json", encoding="utf-8") as jsonData:
        users = json.load(jsonData)
        return users


def get_accounts():
    file = open("excel.txt", "r")
    accounts = [line.strip("\n") for line in file if line != "\n"]
    return accounts


def load_comment():
    with open("comments.json", encoding="utf-8") as jsonData:
        comments = json.load(jsonData)
        comment = choice(comments)
        return comment


def login(driver: Chrome, username, password):
    driver.get("https://truthsocial.com/login")
    sleep(5)

    driver.find_element(By.NAME, "username").send_keys(username)
    sleep(5)
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(
        By.XPATH,
        "/html/body/div/div/main/div/div/div/div/div/div/div[2]/form/div[3]/button",
    ).send_keys(Keys.ENTER)

    print("[I] LOGING BUTTON CLICKED")
    sleep(randint(3, 5))

def delete_user_from_excel(username):
    with open("excel.txt", "r") as file:
        lines = file.readlines()

    with open("excel.txt", "w") as file:
        for line in lines:
            if line.strip("\n") != username:
                file.write(line)

def load_message():
    with open("message.txt", "r", encoding="utf-8") as file:
        message = file.read().replace('\\n', '\n')  # Replace '\\n' with '\n'
    return message



def send_message(driver: Chrome, follower: str):
    driver.get("https://truthsocial.com/chats")
    sleep(5)

    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search Messages']")
    search_box.send_keys(follower)
    sleep(3)

    follower_element_exists = False
    try:
        follower_element = driver.find_element(By.XPATH, "//*[@id='soapbox']/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/button/div/div[2]/p")
        follower_element_exists = True
    except NoSuchElementException:
        pass

    if follower_element_exists:
        follower_element.click()
        sleep(3)

        message = load_message()

        message_box = driver.find_element(By.XPATH, "//textarea[@placeholder='Type a message']")
        message_box.click()  # Click to focus on the message box

        # Send multi-line message by sending each line separately
        for line in message.split('\n'):
            message_box.send_keys(line)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()  # Shift + Enter for a new line
        
        message_box.send_keys(Keys.RETURN)  # Hit Enter key to send the message
        sleep(5)

        print(f"[I] MESSAGE SENT TO: {follower}")
        delete_user_from_excel(follower)
    else:
        print(f"[X] Unable to find element for user: {follower}. Moving to the next user.")
        delete_user_from_excel(follower)
        return





def main():
    users = get_users()
    accounts = get_accounts()
    comments = [load_comment() for _ in range(COMMENT_COUNT)]

    for user in users:
        driver = get_driver()
        login(driver, user['username'], user['password'])

        for account in accounts:
            comment_text = load_comment()
            send_message(driver, account)
        
        driver.quit()

if __name__ == "__main__":
    main()