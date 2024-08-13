from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
import search
import scrap
import save  # Import the new save module
from constants import COUNTIES, url
import os

def handle_alert(driver):
    try:
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert handled and accepted.")
    except NoAlertPresentException:
        pass

def crawl(driver, TABS, START_DATE, END_DATE, SAVE_PATH):
    count_name_index = 0

    while count_name_index < len(COUNTIES):
        tab_handles = []
        for _ in range(min(TABS, len(COUNTIES) - count_name_index)):
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
            tab_handles.append(driver.current_window_handle)
            count_name_index += 1
            if count_name_index >= len(COUNTIES):
                break

        for i, handle in enumerate(tab_handles):
            driver.switch_to.window(handle)
            county_name = COUNTIES[count_name_index - len(tab_handles) + i]
            search.search(driver, county_name, START_DATE, END_DATE)

        for i, handle in enumerate(tab_handles):
            driver.switch_to.window(handle)
            county_name = COUNTIES[count_name_index - len(tab_handles) + i]
            handle_alert(driver)
            results = scrap.scrap(driver)  # Get the results from the scrap function
            save.save_to_spreadsheet(county_name, results, SAVE_PATH)  # Save the results to a spreadsheet
            driver.close()

        driver.switch_to.window(driver.window_handles[0])
