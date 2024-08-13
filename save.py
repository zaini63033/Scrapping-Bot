import os
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

def save_to_spreadsheet(county_name, results, save_path):
    # Define the path to the spreadsheet
    file_path = os.path.join(save_path, "output.xlsx")

    # Check if the spreadsheet already exists
    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
    else:
        workbook = openpyxl.Workbook()

    # Remove the default sheet if it exists
    if "Sheet" in workbook.sheetnames:
        del workbook["Sheet"]

    # Create a new sheet for the county or select the existing one
    if county_name in workbook.sheetnames:
        sheet = workbook[county_name]
    else:
        sheet = workbook.create_sheet(title=county_name)

    # Write headers if the sheet is new
    if sheet.max_row == 1:
        headers = [
            "PT-61", "Sale Date", "Actual Price", "Buyer Name", 
            "Buyer Address", "Seller Name", "Seller Address", 
            "Property Address", "Map & Parcel Number"
        ]
        sheet.append(headers)

        # Bold the headers
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.font = Font(bold=True)

    # Append each result to the sheet
    for record in results:
        sheet.append([
            record["pt61"],
            record["sale_date"],
            record["actual_price"],
            record["buyer_name"],
            record["buyer_address"],
            record["seller_name"],
            record["seller_address"],
            record["property_address"],
            record["map_parcel_number"]
        ])

    # Adjust column widths to fit content
    for column in sheet.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)  # Get the column name
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column_letter].width = adjusted_width

    # Save the workbook
    workbook.save(file_path)
    workbook.close()
