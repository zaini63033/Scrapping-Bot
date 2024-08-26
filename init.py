import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import login
import crawl
from constants import url

def run_scraping_bot(tabs, start_date, end_date, save_path):
    start_time = time.time()

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size to avoid detection issues

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Login
    login.login(driver)

    print('\n')
    crawl.crawl(driver, tabs, start_date, end_date, save_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nRuntime: {elapsed_time} seconds")

    driver.quit()

# Example usage (replace with your actual parameters)
# run_scraping_bot(tabs, start_date, end_date, save_path)
