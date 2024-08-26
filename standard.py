from parse import parse_name, parse_address
from zillow import search_zillow
from maps import search_google_maps

def initialize_driver():
    """
    Initialize the Selenium WebDriver with the necessary options.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def standardize_address(driver, address):
    """
    Standardize the given address using Zillow and Google Maps.
    """

    if address  == "" or address is None:
        return {"address": "", "city": "", "state": "", "zip": "", "country": ""}
    
    print("Searching for ", address, "on zillow.com")

    property_address = search_zillow(driver, address)
    if not property_address["address"]:

        print("Searching for ", address, "on Google Maps")
        property_address = search_google_maps(driver, address)

        if not property_address["address"]:
            print("Result not found, assigning default address!")
            property_address = parse_address(address)
        else:
            print("Address found on Google Maps")
    else:
        print("Address found on Zillow")
    
    return property_address

def parse_record(record, driver):
    """
    Parse and standardize the given record.
    """
    owner_name = parse_name(record["buyer_name"])
    executor_name = parse_name(record["seller_name"])

    owner_address = parse_address(record["buyer_address"])
    executor_address = parse_address(record["seller_address"])
    property_address = standardize_address(driver, record["property_address"])

    return {
        "pt61": record["pt61"],
        "sale_date": record["sale_date"],
        "actual_price": record["actual_price"],
        "owner_name": owner_name,
        "executor_name": executor_name,
        "owner_address": owner_address,
        "executor_address": executor_address,
        "property_address": property_address,
        "map_parcel_number": record["map_parcel_number"]
    }
