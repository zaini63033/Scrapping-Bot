import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import usaddress
from parse import parse_address

def search_google(driver, query):
    """
    Perform a Google search for the given query in the current tab.
    """
    search_url = f"https://www.google.com/search?q={query}"
    driver.get(search_url)

def addresses_match(address1, address2):
    """
    Compare two addresses to check if they have the same address number and street name.
    """
    try:
        parsed1, _ = usaddress.tag(address1)
        parsed2, _ = usaddress.tag(address2)

        address_number1 = parsed1.get('AddressNumber', '')
        street_name1 = parsed1.get('StreetName', '') + ' ' + parsed1.get('StreetNamePostType', '')
        
        address_number2 = parsed2.get('AddressNumber', '')
        street_name2 = parsed2.get('StreetName', '') + ' ' + parsed2.get('StreetNamePostType', '')

        return (address_number1.strip() == address_number2.strip())
    except Exception as e:
        print(f"Error comparing addresses: {e}")
        return False

def search_zillow(driver, property_address):
    """
    Perform a Google search in a new tab to find Zillow results and extract the address from the first Zillow result.
    """
    try:
        # Open a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        # Perform Google search with 'site:zillow.com' parameter in the new tab
        query = f"{property_address} site:zillow.com"
        search_google(driver, query)
        
        # Find all search result titles
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')  # Titles are typically in <h3> tags
        if results:
            # Loop through results and find the first Zillow link
            for result in results:
                link = result.find_element(By.XPATH, '..')
                href = link.get_attribute('href')
                if 'zillow.com' in href:
                    address_title = result.text.split('|')[0].strip()
                    
                    # Compare the address number and street name using the addresses_match function
                    if addresses_match(property_address, address_title):
                        return parse_address(address_title)
    

            return {"address": "", "city": "", "state": "", "zip": ""}
        else:
            return {"address": "", "city": "", "state": "", "zip": ""}
    except Exception as e:
        print(f"Error extracting address from search results of zillow.co: {e}")
        return {"address": "", "city": "", "state": "", "zip": ""}
    finally:
        # Close the new tab and switch back to the original tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
