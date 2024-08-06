from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
import search
import scrap
from constants import COUNTIES, url, TABS

def handle_alert(driver):
    try:
        # Switch to the alert and accept it
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert handled and accepted.")
    except NoAlertPresentException:
        # No alert is present
        pass

def crawl(driver):
    count_name_index = 0  # Keep track of which county we are processing

    while count_name_index < len(COUNTIES):
        # Open up to TABS number of tabs
        tab_handles = []
        for _ in range(min(TABS, len(COUNTIES) - count_name_index)):
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
            tab_handles.append(driver.current_window_handle)
            count_name_index += 1
            if count_name_index >= len(COUNTIES):
                break

        # Perform the search in each tab
        for i, handle in enumerate(tab_handles):
            driver.switch_to.window(handle)
            county_name = COUNTIES[count_name_index - len(tab_handles) + i]
            # Perform the search in the current tab
            search.search(driver, county_name)

        # Scrape the data from each tab
        for i, handle in enumerate(tab_handles):
            driver.switch_to.window(handle)
            county_name = COUNTIES[count_name_index - len(tab_handles) + i]
            # Handle any unexpected alerts before scraping
            handle_alert(driver)
            # Scrape the data from the results page
            scrap.scrap(driver, county_name)
            
            # Close the tab
            try:
                driver.close()
            except UnexpectedAlertPresentException:
                # Handle the alert if it appears again during tab close
                handle_alert(driver)
                driver.close()

        # Switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])
        
        
