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
        number = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*/main/section[5]/div[2]/div/div/div[1]/p/span[1]"))
        ).text.replace(" followers","")
        return number

    def make_follow(self,driver,account,followers,number_of_accounts):
        for url in account:
            try:
                driver.get(url)
                time.sleep(2)
                if self.check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[2]/div[1]/div[3]/button'):
                    time.sleep(1)
                    if self.check_exists_by_xpath(driver,'//*/main/section[1]/div[2]/div[3]/div/button[1]'):
                        if driver.find_element(By.XPATH,'//*/main/section[1]/div[2]/div[3]/div/button[1]').text == "Follow":
                            time.sleep(1)
                            follow = driver.find_element(By.XPATH,'//*/main/section[1]/div[2]/div[3]/div/button[1]').click()
                            
                            name = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1').text
                            self.write(name)
                            followers+=1
                            print("follower in if: ",followers)
                            if followers == number_of_accounts:
                                return followers
                else:
                    number_followers = self.show_number_of_followers(driver)

                    print(number_followers)

                    reaction1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[1]/div/div/div[2]/div/div/ul/li[1]/button/span')).text)
                    reaction2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[2]/div/div/div[2]/div/div/ul/li[1]/button/span')).text)
                    reaction3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*/div[4]/div/div/div[1]/ul/li[3]/div/div/div[3]/div/div/ul/li[1]/button/span')).text)

                    print(reaction1)
                    print(reaction2)
                    print(reaction3)


                    # mean = (reaction1 + reaction2 + reaction3)//3
                    # print(mean)

                    # if mean/number_followers > 0.25:
                    #     if self.check_exists_by_xpath(driver,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]'):
                    #         if driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]').text == "Follow":
                    #             follow = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]').click()
                                
                    #             name = driver.find_element(By.XPATH,'//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1').text
                    #             self.write(name)
                    #             followers+=1
                    #             print("follower in elif: ",followers)
                    #             if followers == number_of_accounts:
                    #                 return followers
            except:
                print("error")
                time.sleep(5)
        return followers



    def follow(self):
        skill = get_skill()
        driver = self.inisialise_driver()
        self.search(skill,driver)
        number_of_accounts = 20
        followers = 0
        account = self.get_accounts_links(driver)
        followers = self.make_follow(driver,account,followers,number_of_accounts)
        print("follower : ",followers)
        page = 12
        while followers < number_of_accounts:
            page+=1
            if self.next_page(driver,page,skill):
                account = self.get_accounts_links(driver)
                print(account)
                followers = self.make_follow(driver,account,followers,number_of_accounts)
                print("follower : ",followers)
            else:
                print("no such accounts")
                break

        time.sleep(5)


my_account = Linkdin()
my_account.follow()