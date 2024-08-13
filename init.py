import time
from selenium import webdriver
import login
import crawl
from constants import url

def run_scraping_bot(tabs, start_date, end_date, save_path):
    start_time = time.time()

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    # Login
    login.login(driver)

    print('\n')
    crawl.crawl(driver, tabs, start_date, end_date, save_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nRuntime: {elapsed_time} seconds")

    time.sleep(100)
    driver.quit()
