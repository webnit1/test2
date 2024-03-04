import os
import sys
import json
import glob
import logging
import pyautogui
from time import sleep
from random import randint, choice
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

COMMENT_COUNT = 25 # this count stands for your rotation count
DELAY = 10

logging.basicConfig(level=logging.INFO, filename='LogFile.log',
                    filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def get_driver():
    options = Options()
    # options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--lang=en-US")
    options.add_argument("start-maximized")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(service=Service(CM().install()), options=options)
    driver.implicitly_wait(DELAY)
    driver.maximize_window()

    return driver

def get_users():
    with open('accounts.json', encoding="utf-8") as jsonData:
        users = json.load(jsonData)
        return users


def get_accounts():
    file = open("excel.txt", "r")
    accounts = [line.strip("\n") for line in file if line != "\n"]
    return accounts

    print(YourString.encode('ascii', 'replace').decode('ascii'))


def load_comment():
    with open('comments.json', encoding="utf-8") as jsonData:
        comments = json.load(jsonData)
        comment = choice(comments)
        return comment


def login(driver:Chrome, username, password):
    driver.get("https://truthsocial.com/login")
    sleep(5)

    driver.find_element(By.NAME, "username").send_keys(username)
    sleep(5)
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.XPATH, "/html/body/div/div/main/div/div/div/div/div/div/div[2]/form/div[3]/button").send_keys(Keys.ENTER)

    print("[I] LOGING BUTTON CLICKED")
    sleep(randint(3,5))

def scroll():
    pass

def list_to_text_file(list_1,filename):
    with open(f"followers_list_"+str(filename)+".txt", "a", encoding='utf-8-sig') as file:
        for a in list_1:
            file.write(a)
            file.write('\n')

def main(): # first main function is compiled. ok?
    users = get_users() # this part is that we take all users from account.json file

    print(f"[INFO] LOADED {len(users)} USER ACCOUNTS TO MAKE COMMENTS ON NEW POSTS")
    for idxi, user in enumerate(users):
        try:
            driver = get_driver()
            sleep(1)
            username = user["username"]
            sleep(1)
            password = user["password"]
            sleep(1)
            comment_text = load_comment()
            sleep(5)
            print(f"[INFO][{idxi}/{len(users)}] LOGGINNG IN TO THE USER :- ", username)
            login(driver, username, password)
            if driver.current_url == 'www.google.com':
                pass
            else:
                sleep(5)
                driver.get('https://truthsocial.com/@' + username + '/followers')
                #webpage_scroll(driver,scroll_limit=None)
                sleep(1)
                followers = []
                for a in range(7000):
                    followers = followers + driver.execute_script("return(get());function get(){var arr = []; for (let i=0; i<document.getElementsByTagName('p').length; i++){var d = document.getElementsByTagName('p')[i].innerText; if(d.includes('@')){arr.push(d);}} return arr;} get()")
                    sleep(0.2)
                    code = 'driver.execute_script("window.scrollTo(0, ' + str(a*10) + ')")'
                    exec(code)
                followers_final = list(set(followers))
                print(len(followers_final))
                list_to_text_file(followers_final,filename=username)
                # for b in followers_final:
                #     driver.get('https://truthsocial.com/' + b)
                #     sleep(7)
                #     code = 'driver.execute_script("window.scrollTo(0, 0)")'
                #     exec(code)
                #     sleep(4)
                #     try:
                #         message = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[1]/div/main/div/div/div/div/div[1]/div[2]/div/div[2]/div/button[2]")
                #         message.click()
                #     except:
                #         print('not fo7')
                #         pass

                #     try:
                #         message = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[1]/div/main/div/div/div/div/div[1]/div[2]/div/div[2]/div/button[3]")
                #         message.click()
                #     except:
                #         print('not fo7')
                #         pass
                #     sleep(5)

                # def canvas_element(driver):
                #     # download button
                #     action = ActionChains(driver)
                #     try:
                        
                #         ta = driver.execute_script("return document.querySelectorAll('textarea')[0].innerHTML = arguments[0];",'Hello Dear Patriot how are you doing?\nTHE STORM OF THE CENTURY IS COMING...\n IF YOU KNOW, YOU KNOW.\nThe right channel at the right time! This is no joke - If you are scared, do not join!\nDO YOU MISS VICTORY?\n- THE TIME HAS COME.\nThe enormity of what is coming will blow you away. JOIN IMMEDIATELY\nhttps://bit.ly/TRUMP_EXPLICIT')
                #         sleep(2)
                #         action.key_down(Keys.SPACE).perform()
                #         sleep(2)
                #         action.key_down(Keys.ENTER).perform()
                        
                #     except Exception as e:
                #         print(e)
                # canvas_element(driver=driver)
                # sleep(5)
                print('\n\n')
        except Exception as e:
            print(e)


main()
