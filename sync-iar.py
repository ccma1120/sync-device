import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import difflib

# URL to parse
url = "https://updates.iar.com/FileStore/STANDARD/001/003/381/arm/doc/infocenter/device_support/Nuvoton.ENU.html"

# Output file names
device_file = "device-iar.txt"
compare_file = "compare-iar.txt"

# Fetch the page
response = requests.get(url)
if response.status_code != 200:
    print(f"Error fetching URL: {response.status_code}")
    exit()

html_content = response.text

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Initialize an empty list for devices
devices = []

# Try to find device names in list items (<li> tags)
list_items = soup.find_all("li")
for li in list_items:
    text = li.get_text(strip=True)
    if text:
        devices.append(text)

# If no devices found in <li>, try table rows (<tr> tags)
if not devices:
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if cells:
            device = cells[0].get_text(strip=True)
            if device:
                devices.append(device)

# Prepare the new content as a list of lines (strip trailing spaces)
new_lines = [line.strip() for line in devices if line.strip()]

# If the device file exists, back it up and compare with the new content.
if os.path.exists(device_file):
    # Read the old content from backup file
    with open(device_file, "r", encoding="utf-8") as f:
        old_lines = [line.rstrip() for line in f.readlines()]
    
    # Compare old and new lists using difflib
    diff = difflib.unified_diff(old_lines, new_lines, fromfile=device_file, tofile=device_file, lineterm="")
    diff_lines = list(diff)
    
    if diff_lines:
        # Create timestamp and backup files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"device_iar{timestamp}.txt"
        compare_file = f"compare_iar{timestamp}.txt"
        os.rename(device_file, backup_file)
        print(f"Backup created: {backup_file}")
        
        # Write new device list to device_file
        with open(device_file, "w", encoding="utf-8") as f:
            for line in new_lines:
                f.write(line + "\n")
        print(f"New device list saved to '{device_file}'.")
        
        # Write differences to compare file
        with open(compare_file, "w", encoding="utf-8") as f:
            for line in diff_lines:
                f.write(line + "\n")
        print(f"Differences saved to '{compare_file}'.")
    else:
        print("No differences found. No files were modified.")
else:
    # If no device file exists, simply write the new list.
    with open(device_file, "w", encoding="utf-8") as f:
        for line in new_lines:
            f.write(line + "\n")
    print(f"Device list saved to '{device_file}'.")
