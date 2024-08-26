from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parse import parse_address

def search_google_maps(driver, location):
    """
    Perform a search on Google Maps for the given location in a new tab and return the parsed address.
    """
    try:
        # Open a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        # Navigate to Google Maps
        maps_url = "https://www.google.com/maps"
        driver.get(maps_url)

        # Find the search input field and enter the location
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(location)
        
        # Find the search button and click it
        search_button = driver.find_element(By.ID, "searchbox-searchbutton")
        search_button.click()

        # Wait for the address element to be present and extract the address
        try:
            # WebDriverWait to wait until the address element is loaded
            wait = WebDriverWait(driver, 10)
            address_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label and contains(@aria-label, 'Address')]"))
            )
            place_address = address_element.get_attribute("aria-label").replace("Address, ", "")
            return parse_address(place_address)
        except Exception as e:
            print(f"Could not extract address: {e}")
            return {"address": "", "city": "", "state": "", "zip": ""}
    
    except Exception as e:
        print(f"Error during Google Maps search: {e}")
        return {"address": "", "city": "", "state": "", "zip": ""}
    
    finally:
        # Close the new tab and switch back to the original tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
