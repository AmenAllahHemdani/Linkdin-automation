from linkedin_scraper import JobSearch, actions
from selenium import webdriver

driver = webdriver.Chrome("/Users/softylines/Desktop/scrapping/Linkdin/chromedriver")
email = "raedakkari324@gmail.com"
password = "doliprane"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
input("Press Enter")
job_search = JobSearch(driver=driver, close_on_complete=False, scrape=False)
# job_search contains jobs from your logged in front page:
# - job_search.recommended_jobs
# - job_search.still_hiring
# - job_search.more_jobs

job_listings = job_search.search("Machine Learning Engineer")