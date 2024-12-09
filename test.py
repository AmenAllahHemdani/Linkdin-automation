from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import json
import pickle
from get_skill import get_skill


def inisialise_driver():
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        driver = webdriver.Chrome()
        driver.get("https://www.linkedin.com/feed/")
        for cookie in cookies:
            driver.add_cookie(cookie)
        return driver


def show_number_of_followers(driver):
    try:
        number = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*/main/section[1]/div[2]/ul/li/span "))).text.replace(" followers","")       
        return number.replace(",","") 
    except:
        print("error")

def engagement(driver):
        number_followers = int(show_number_of_followers(driver))

        print(number_followers)

        reaction1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[1]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")
        reaction2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[2]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")
        reaction3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[3]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")

        mean = (int(reaction1)+int(reaction2)+int(reaction3))//3

        if mean >= (number_followers//100):
            return True
        else:
            return False


driver = inisialise_driver()
driver.get("https://www.linkedin.com/in/demishassabis/")
print(engagement(driver))