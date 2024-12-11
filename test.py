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

def check_exists_by_xpath(driver,xpath):
        try:
            driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
        return True

def make_connect(driver,url):
        try:
            driver.get(url)
            time.sleep(1)
            if check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[2]/div[1]/div[3]/button'):
                name = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1').text
                if check_exists_by_xpath(driver,"//*/main/section[1]/div[2]/div[3]/div/button/span[text()='Connect']"):
                    print("connect found")
                    connect = driver.find_element(By.XPATH,'//*/main/section[1]/div[2]/div[3]/div/button[1]').click()
                    send = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Send']"))).click()
                    time.sleep(2)
                    print("Connect  :  "+name)
                    return 1
                
                elif check_exists_by_xpath(driver,"//*/main/section[1]/div[2]/div[3]/div/button/span[text()='Follow']"):
                    print("here")
                    if check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[3]/div/div[2]/button/span[text()=\'More\']'):
                        print("1")
                        more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*/main/section[1]/div[2]/div[3]/div/div[2]/button/span[text()=\'More\']"))).click()
                        print("2")
                        time.sleep(1)
                        connect_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div/span[text()='Connect']"))).click()
                        print("3")
                        send = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Send']"))).click()
                        print('4')
                        print("Connect  :  "+name)
                        return 1
        except:
            print("error")
        return 0


def show_number_of_followers(driver):
        number = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*/main/section[1]/div[2]/ul/li[1]/span"))
        ).text.replace(" followers","")

        return number.replace(",","")

def engagement(driver):
        # try:
            number_followers = int(show_number_of_followers(driver))
            print(number_followers)

            reaction1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[1]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")
            reaction2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[2]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")
            reaction3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[3]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")

            print(reaction1)
            print(reaction2)
            print(reaction3)

            mean = (int(reaction1)+int(reaction2)+int(reaction3))//3

            if mean >= (number_followers//100) and number_followers > 10000:
                return True
            else:
                return False 
        # except:
        #     print('reaction anf followers not found')
        #     return False

driver = inisialise_driver()
driver.get("https://www.linkedin.com/in/helenpamely/")
print(engagement(driver))