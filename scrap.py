from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import parse
import re

def scrap(driver):
    # Set up WebDriverWait
    wait = WebDriverWait(driver, 10)
    
    try:
        # Find all table rows
        rows = driver.find_elements(By.XPATH, "//tr")
        
        results = []
        
        for row in rows:
            try:
                # Find elements within the same row
                pt61_element = row.find_element(By.XPATH, ".//*[contains(text(), '-')]")
                sale_date_element = row.find_element(By.XPATH, ".//*[contains(text(), 'Sale Date')]")
                sale_price_element = row.find_element(By.XPATH, ".//*[contains(text(), 'Sale Price')]")
                
                pt61_text = pt61_element.text
                sale_date_text = sale_date_element.text
                sale_date = parse.parse_sale_date(sale_date_text)
                sale_price_text = sale_price_element.text
                actual_price = parse.parse_price(sale_price_text)
                
                # Validate PT-61 format and actual price
                if not re.match(r'\d{3}-\d{4}-\d{6}', pt61_text) or actual_price > 100:
                    continue
                
                # Click the row to open detailed information
                row.click()
                
                # Switch to the frame or modal
                try:
                    # Wait for the frame or modal to appear
                    wait.until(EC.presence_of_element_located((By.XPATH, "//iframe")))  # Adjust the XPath if necessary
                    iframe = driver.find_element(By.XPATH, "//iframe")  # Adjust the XPath if necessary
                    driver.switch_to.frame(iframe)
                    
                    # Extract specific elements using the provided XPaths
                    buyer_name = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/div/table[2]/tbody/tr[2]/td/span[1]").text.strip()
                    buyer_address = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/div/table[2]/tbody/tr[2]/td/span[2]").text.strip()
                    seller_name = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/div/table[3]/tbody/tr[2]/td/span[1]").text.strip()
                    seller_address = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/div/table[3]/tbody/tr[2]/td/span[2]").text.strip()
                    property_address = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/div/table[4]/tbody/tr[2]/td[1]/span").text.strip()
                    map_parcel_number = driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/div/table[4]/tbody/tr[2]/td[3]/span").text.strip()
                    
                    # Append the results to the list
                    results.append({
                        "pt61": pt61_text,
                        "sale_date": sale_date,
                        "actual_price": actual_price,
                        "buyer_name": buyer_name,
                        "buyer_address": buyer_address,
                        "seller_name": seller_name,
                        "seller_address": seller_address,
                        "property_address": property_address,
                        "map_parcel_number": map_parcel_number
                    })
                    
                    # Close the frame or modal
                    driver.switch_to.default_content()  # Switch back to the default content
                    close_button = driver.find_element(By.XPATH, "//button[@title='Close']")  # Locate button by title attribute
                    close_button.click()
                    
                except Exception as e:
                    print(f"Error while handling frame/modal: {e}")
                    driver.switch_to.default_content()  # Ensure we return to default content in case of error
                
            except Exception as e:
                # Continue to the next row if any element is not found in the current row
                continue
        
        return results
    
    except Exception as e:
        print(f"Error: {e}")
        return []
