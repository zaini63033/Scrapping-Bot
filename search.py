from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from constants import START_DATE, END_DATE

def search(driver, county_name):
    try:
        # Wait for the page to load and locate the instrument type dropdown
        wait = WebDriverWait(driver, 5)
        instrument_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BodyContent_ddlInstrumentTypes")))

        # Select an option from the instrument type dropdown
        select_instrument_type = Select(instrument_type_dropdown)
        select_instrument_type.select_by_visible_text("DEED - FROM ESTATE")
    except Exception as e:
        logging.error(f"Error selecting instrument type: {e}")

    try:
        # Wait for the county dropdown to become clickable
        county_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BodyContent_ddlCounties")))

        # Select an option from the county dropdown
        select_county = Select(county_dropdown)
        select_county.select_by_visible_text(county_name)
    except Exception as e:
        logging.error(f"Error selecting county: {e}")

    try:
        # Locate and set the start date
        start_date = driver.find_element(By.ID, "txtDateFrom")
        start_date.clear()
        start_date.send_keys(START_DATE)
    except Exception as e:
        logging.error(f"Error setting start date: {e}")

    try:
        # Locate and set the end date
        end_date = driver.find_element(By.ID, "txtDateTo")
        end_date.clear()
        end_date.send_keys(END_DATE)
    except Exception as e:
        logging.error(f"Error setting end date: {e}")

    # try:
    #     # Locate and tick the expand dashboard results checkbox
    #     expand_checkbox = driver.find_element(By.ID, "BodyContent_chkExpand")
    #     if not expand_checkbox.is_selected():
    #         expand_checkbox.click()
    # except Exception as e:
    #     logging.error(f"Error clicking expand checkbox: {e}")

    try:
        # Submit the form to get the results
        submit_button = driver.find_element(By.ID, "BodyContent_btnSearch")
        submit_button.click()
        
    except Exception as e:
        logging.error(f"Error submitting the form or waiting for results: {e}")

