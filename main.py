from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import pickle
from get_skill import get_skill


class Linkdin:

    def write(self,data):
        f = open("follow.txt", "a")
        f.write(data+"\n")
        f.close()


    def check_exists_by_xpath(self,driver,xpath):
        try:
            driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
        return True


    def search(self,skill,driver):
        driver.get(f"https://www.linkedin.com/search/results/people/?keywords={skill}%20Top%20voice")
        return driver


    def get_len_accounts(self,driver):
        li = driver.find_elements(By.XPATH,"//*/div/div/ul/li")
        return len(li)


    def next_page(self,driver,i,skill):
        try:
            driver.get(f'https://www.linkedin.com/search/results/people/?keywords={skill}%20Top%20voice&origin=GLOBAL_SEARCH_HEADER&page={i}&sid=wIb')
            return True
        except:
            return False


    def inisialise_driver(self):
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        driver = webdriver.Chrome()
        driver.get("https://www.linkedin.com/feed/")
        for cookie in cookies:
            driver.add_cookie(cookie)
        return driver


    def get_accounts_links(self,driver):
        n = self.get_len_accounts(driver)
        print("n = ",n)
        account = []
        time.sleep(1)
        for i in range(1, n+1):
            try:
                peoples_accounts = driver.find_element(By.XPATH, f'//*//div/div/ul/li[{i}]/div/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a')
                url = "https://www.linkedin.com/search/results/people/"
                if url not in peoples_accounts.get_attribute('href'):
                    account.append(peoples_accounts.get_attribute('href'))
            except Exception as e:
                print(f"Error processing element {i}")
        return account
        

    def show_number_of_followers(self, driver):
        number = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*/main/section[5]/div[2]/div/div/div[1]/p/span[1]"))
        ).text.replace(" followers","")
        return number

    def engagement(self,driver):
        number_followers = int(self.show_number_of_followers(driver))

        reaction1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[1]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")
        reaction2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[2]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")
        reaction3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[3]/div/div/div[last()-1]/div/div/ul/li[1]/button/span'))).text.replace(",","")

        mean = (int(reaction1)+int(reaction2)+int(reaction3))//3

        if mean >= (number_followers//100) and number_followers > 10000:
            return True
        else:
            return False 

    def make_follow(self,driver,url):
        try:
            driver.get(url)
            time.sleep(1)
            name = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1').text
            if self.check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[2]/div[1]/div[3]/button') or self.engagement(driver):
                time.sleep(1)
                if self.check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[3]/div/button[1]'):
                    if driver.find_element(By.XPATH,'//*/main/section[1]/div[2]/div[3]/div/button[1]').text == "Follow":
                        time.sleep(1)
                        follow = driver.find_element(By.XPATH,'//*/main/section[1]/div[2]/div[3]/div/button[1]').click()
                        self.write("Follow  :  "+name)
                        return 1
                    
        except:
            print("error")
        return 0

    def make_connect(self,driver,url):
        try:
            driver.get(url)
            time.sleep(1)
            if self.check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[2]/div[1]/div[3]/button') or self.engagement(driver):
                time.sleep(1)
                name = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1').text
                if self.check_exists_by_xpath(driver,"//*/main/section[1]/div[2]/div[3]/div/button/span[text()='Connect']"):
                    connect = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*/main/section[1]/div[2]/div[3]/div/button/span[text()=\'Connect\']'))).click()
                    time.sleep(1)
                    send = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Send']"))).click()
                    self.write("Connect  :  "+name)
                    return 1
                    
                elif self.check_exists_by_xpath(driver,"//*/main/section[1]/div[2]/div[3]/div/button/span[text()='Follow']"):
                    if self.check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[3]/div/div[2]/button/span[text()=\'More\']'):
                        more = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*/main/section[1]/div[2]/div[3]/div/div[2]/button/span[text()=\'More\']"))).click()
                        time.sleep(1)
                        connect = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div/span[text()='Connect']"))).click()
                        time.sleep(1)
                        send = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Send']"))).click()
                        self.write("Connect  :  "+name)
                        return 1

        except:
            print("error")
        return 0


    def connect(self):
        skill = get_skill()
        driver = self.inisialise_driver()
        self.search(skill,driver)
        number_of_accounts = 5
        Connects = 0
        page = 4
        while Connects < number_of_accounts:
            page+=1
            if self.next_page(driver,page,skill):
                account = self.get_accounts_links(driver)
                for url in account:
                    Connects += self.make_connect(driver,url)
                    if Connects == number_of_accounts:
                        break
            else:
                print("no such accounts")
                break


    def follow(self):
        skill = get_skill()
        driver = self.inisialise_driver()
        self.search(skill,driver)
        number_of_accounts = 3
        followers = 0
        page = 0
        while followers < number_of_accounts:
            page+=1
            if self.next_page(driver,page,skill):
                account = self.get_accounts_links(driver)
                for url in account:
                    followers += self.make_follow(driver,url)
                    if followers == number_of_accounts:
                        break
            else:
                print("no such accounts")
                break


    def follow_connect(self):
        skill = get_skill()
        driver = self.inisialise_driver()
        self.search(skill,driver)
        number_of_accounts = 3
        followers = 0
        connects = 0
        page = 6
        while followers < number_of_accounts and connects < number_of_accounts:
            page+=1
            if self.next_page(driver,page,skill):
                account = self.get_accounts_links(driver)
                for url in account:
                    followers += self.make_follow(driver,url)
                    connects += self.make_connect(driver,url)
                    if followers == number_of_accounts and connects == number_of_accounts:
                        break
            else:
                print("no such accounts")
                break
        print("followers are complited")


my_account = Linkdin()
my_account.follow_connect()