import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import difflib

# URL to parse
url = "https://www.segger.com/supported-devices/nuvoton/"

# Output file names
device_file = "device-segger.txt"
compare_file = "compare-segger.txt"

# Fetch the page
response = requests.get(url)
if response.status_code != 200:
    print(f"Error fetching URL: {response.status_code}")
    exit()

html_content = response.text

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Initialize an empty list for device names
devices = []

# --- Extraction Logic ---
# Try 1: Look for devices in table rows (if there's a table)
table = soup.find("table")
if table:
    rows = table.find_all("tr")
    for row in rows:
        # Assume device name is in the first table cell
        cells = row.find_all("td")
        if cells:
            device = cells[0].get_text(strip=True)
            if device:
                devices.append(device)

# Try 2: If no devices extracted, try to look for device names in link texts
if not devices:
    links = soup.find_all("a")
    for link in links:
        text = link.get_text(strip=True)
        if text:
            devices.append(text)

# Remove duplicates and empty lines
new_lines = list(dict.fromkeys([line.strip() for line in devices if line.strip()]))

# --- Backup and Compare ---
if os.path.exists(device_file):
    # Backup the original file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"device_segger{timestamp}.txt"
    os.rename(device_file, backup_file)
    print(f"Backup created: {backup_file}")
    
    # Read the old content from the backup file
    with open(backup_file, "r", encoding="utf-8") as f:
        old_lines = [line.rstrip() for line in f.readlines()]
    
    # Write the new device list to device_file
    with open(device_file, "w", encoding="utf-8") as f:
        for line in new_lines:
            f.write(line + "\n")
    print(f"New device list saved to '{device_file}'.")
    
    # Compare the old and new lists using difflib
    diff = difflib.unified_diff(old_lines, new_lines, fromfile=backup_file, tofile=device_file, lineterm="")
    diff_lines = list(diff)
    
    # Write differences to compare_file
    with open(compare_file, "w", encoding="utf-8") as f:
        for line in diff_lines:
            f.write(line + "\n")
    print(f"Comparison saved to '{compare_file}'.")
else:
    # If no device-segger.txt exists, simply write the new list.
    with open(device_file, "w", encoding="utf-8") as f:
        for line in new_lines:
            f.write(line + "\n")
    print(f"Device list saved to '{device_file}'.")
