from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import spacy
import usaddress

# Load SpaCy's English language model
nlp = spacy.load('en_core_web_sm')

def parse_price(price_string):
    # Use regular expression to extract numeric value from the string
    match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_string)
    if match:
        # Remove commas and convert to integer
        price_numeric = match.group(1).replace(',', '')
        return int(float(price_numeric))  # Convert to float first to handle decimal points
    return None

def parse_sale_date(sale_date_string):
    # Use regular expression to extract sale date from the string
    match = re.search(r'Sale Date:\s*(\d{1,2}/\d{1,2}/\d{4})', sale_date_string)
    if match:
        return match.group(1)  # Return the sale date
    return None

def parse_name(name_string):
    # Process the name string with SpaCy
    doc = nlp(name_string)

    # Initialize the parts of the name
    first_name = middle_name = last_name = suffix = None

    # Iterate over the entities in the processed document
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Split the person's name into components
            name_parts = ent.text.split()
            if len(name_parts) == 1:
                first_name = name_parts[0]
            elif len(name_parts) == 2:
                first_name, last_name = name_parts
            elif len(name_parts) >= 3:
                first_name = name_parts[0]
                last_name = name_parts[-1]
                middle_name = " ".join(name_parts[1:-1])
            break

    return {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'suffix': suffix 
    }


def parse_address(address_title):
    """
    Parse the address title into components: address, city, state, and ZIP code using usaddress.
    """
    try:
        # Attempt to parse the address
        parsed_address, address_type = usaddress.tag(address_title)
        
        # Directly access the parsed address components
        address = f"{parsed_address.get('AddressNumber', '')} {parsed_address.get('StreetName', '')} {parsed_address.get('StreetNamePostType', '')}".strip()
        city = parsed_address.get('PlaceName', '').strip()
        state = parsed_address.get('StateName', '').strip()
        zip_code = parsed_address.get('ZipCode', '').strip()
        
        return {
            'address': address,
            'city': city,
            'state': state,
            'zip': zip_code
        }
    
    except usaddress.RepeatedLabelError as e:
        # Handle repeated labels by considering only the first occurrence
        parsed_address = e.parsed_string
        print(f"Warning: Ambiguous address components detected. Using first occurrence only.")
        
        # Extract first occurrences manually
        address_number = next((token for token, label in parsed_address if label == 'AddressNumber'), '')
        street_name = next((token for token, label in parsed_address if label == 'StreetName'), '')
        street_name_post_type = next((token for token, label in parsed_address if label == 'StreetNamePostType'), '')
        city = next((token for token, label in parsed_address if label == 'PlaceName'), '')
        state = next((token for token, label in parsed_address if label == 'StateName'), '')
        zip_code = next((token for token, label in parsed_address if label == 'ZipCode'), '')
        
        address = f"{address_number} {street_name} {street_name_post_type}".strip()
        
        return {
            'address': address,
            'city': city.strip(),
            'state': state.strip(),
            'zip': zip_code.strip()
        }

    except Exception as e:
        print(f"Error parsing address using usaddress: {e}")
        return {
            'address': address_title,
            'city': '',
            'state': '',
            'zip': ''
        }
