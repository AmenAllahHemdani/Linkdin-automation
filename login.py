from selenium import webdriver
from selenium.webdriver.common.by import By 
import time
import json
import pickle


def load_cookies(driver):
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

def Login():
    email = "firastuiti@gmail.com"
    password = 'firastuiti123'
    
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login/")

    email_input = driver.find_element(By.XPATH,"//*[@id='username']")
    email_input.send_keys(email)


    password_input = driver.find_element(By.XPATH,'//*[@id="password"]')
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[4]/button').click()
    time.sleep(10)


    load_cookies(driver)

    driver.get("https://www.linkedin.com/feed/")

Login()   


#https://www.linkedin.com/search/results/people/?keywords=Frontend%20Top%20voice
#https://www.linkedin.com/search/results/people/?keywords=backend%20Top%20voice