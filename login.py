from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import username, password

def login(driver):
    # Wait for the username and password fields to be present
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "txtUserID")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "txtPassword")))

    # Enter the username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    login_button = driver.find_element(By.NAME, "logon")
    login_button.click()

