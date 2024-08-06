import re

def parse_price(price_string):
    # Use regular expression to extract numeric value from the string
    match = re.search(r'\$([\d,]+(?:\.\d{2})?)', price_string)
    if match:
        # Remove commas and convert to integer
        price_numeric = match.group(1).replace(',', '')
        return int(float(price_numeric))  # Convert to float first to handle decimal points
    return None

def parse_sale_date(price_string):
    # Use regular expression to extract sale date from the string
    match = re.search(r'Sale Date:\s*(\d{1,2}/\d{1,2}/\d{4})', price_string)
    if match:
        return match.group(1)  # Return the sale date
    return None
