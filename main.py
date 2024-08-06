from selenium import webdriver
import login
import time
import crawl
from constants import url

start_time = time.time()

# Set up the web driver
driver = webdriver.Edge()  # or use webdriver.Firefox(), webdriver.Chrome(), etc.
driver.maximize_window()
driver.get(url)

# Login
login.login(driver)

print('\n')
crawl.crawl(driver)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nRuntime: {elapsed_time} seconds")

time.sleep(100)
# Close the driver
driver.quit()
