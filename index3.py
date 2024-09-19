import cv2
import pytesseract
import csv
import re

# Load the image
image = cv2.imread('form.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Tesseract to extract text
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray, config=custom_config)

# Define patterns to search for the required fields
patterns = {
    "Client's Number": r"Client's Number:\s*(.*)",
    "Client's Name": r"Client's Name:\s*(.*)",
    "Payment Date": r"Payment Date:\s*(.*)"
}

# Extract the data using the patterns
extracted_data = {}
for key, pattern in patterns.items():
    match = re.search(pattern, text)
    extracted_data[key] = match.group(1).strip() if match else 'N/A'

# Handle the table part (Amount Paid, Remaining Balance, Remarks)
# Adjusted to capture the value to the right of each header
table_data_pattern = r"Amount Paid\s*K\s*([\d,\.]+)\s*Remaining Balance\s*K\s*([\-\d,\.]+)\s*Remarks\s*(.*)"

table_match = re.search(table_data_pattern, text)

if table_match:
    extracted_data["Amount Paid"] = "K " + table_match.group(1).strip()
    extracted_data["Remaining Balance"] = "K " + table_match.group(2).strip()
    extracted_data["Remarks"] = table_match.group(3).strip()
else:
    extracted_data["Amount Paid"] = 'N/A'
    extracted_data["Remaining Balance"] = 'N/A'
    extracted_data["Remarks"] = 'N/A'

# Open or create the CSV file and write data with headers
csv_file = 'extracted_data.csv'
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)

    # Check if the file is empty and write the headers
    if file.tell() == 0:
        writer.writerow(["Client's Number", "Client's Name", "Payment Date", "Amount Paid", "Remaining Balance", "Remarks"])

    # Write the extracted data as a row
    writer.writerow([
        extracted_data["Client's Number"],
        extracted_data["Client's Name"],
        extracted_data["Payment Date"],
        extracted_data["Amount Paid"],
        extracted_data["Remaining Balance"],
        extracted_data["Remarks"]
    ])

print("Relevant data has been successfully written to 'extracted_data.csv'")
