from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import parse

def scrap(driver, county_name):
    # Set up WebDriverWait
    wait = WebDriverWait(driver, 5)
    
    try:
        # Scrap the Actual Price and Sale Date
        date_price_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr/td[2]/div/div/div[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div[2]/table/tbody/tr[1]/td[6]/span")))
    except:
        return False
    
    date_price_text = date_price_element.text
    
    # Extract Actual Price
    actual_price = parse.parse_price(date_price_text)
    
    # if actual_price is None or actual_price < 0 or actual_price > 100:
    #     return False
    
    print(county_name)
    print("Actual Price: ", actual_price)

    # Extract Sale Date
    sale_date = parse.parse_sale_date(date_price_text)
    print("Sale Date: ", sale_date)
    
    try:
        # Scrap the PT-61 data
        pt61_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr/td[2]/div/div/div[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div[2]/table/tbody/tr[1]/td[4]/span")))
    except:
        return False
    
    pt61_number = pt61_element.text
    print("PT-61: ", pt61_number)
    
    # try:
    #     # Click on the division to reveal additional information
    #     division_element = wait.until(EC.element_to_be_clickable((By.ID, "pnlXRef1")))
    #     division_element.click()
    # except:
    #     return False
    
    
    # try:
    #     # Capture all text within the division
    #     division_text = driver.find_element(By.ID, "pnlXRef1").text
    #     print("Division Text: ", division_text)
    # except:
    #     return False
    
    print('\n')
    return True
