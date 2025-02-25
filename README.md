

# DGDA Allopathic Products Data Scraper

This Python script scrapes data from the **DGDA Allopathic Products** page and saves it into an Excel file for further analysis. It uses **Selenium** for browser automation and **Pandas** for data handling. This script is useful for collecting information on allopathic products registered with the DGDA.

## Features:
- **Headless Browsing**: Runs without opening the browser window, making the process more efficient.
- **Data Scraping**: Collects all product details from the DGDA Allopathic Products page.
- **Pagination Handling**: Automatically navigates through all pages to scrape the entire dataset.
- **Excel Export**: Saves the scraped data to an Excel file, updating it every 100 rows to avoid memory overload.
- **Error Handling**: Gracefully exits if the table or pagination elements are not found, and provides error messages.

## Requirements:
Before running this script, make sure you have the following installed:

- **Python 3.x**: Ensure Python is installed on your system.
- **Selenium**: To automate the web browser interaction.
- **Pandas**: For data manipulation and saving the collected data into an Excel file.

You can install the required dependencies using the following command:

```bash
pip install selenium pandas
```

Additionally, you'll need **Microsoft Edge WebDriver** to run this script. You can download the WebDriver that matches your version of Microsoft Edge from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

## Setup:

1. **WebDriver Path**:  
   Ensure that the **Edge WebDriver** (msedgedriver.exe) is located at:  
   `"C:\Users\Dell\Downloads\msedgedriver.exe"`. If it's located elsewhere, update the `edge_driver_path` variable in the script accordingly.

2. **Output Path**:  
   The collected data will be saved as an Excel file at:  
   `"C:\Users\Dell\Downloads\dgda_allopathic_products.xlsx"`.  
   You can change this path to any location you'd prefer.

## How to Use:

1. **Update Paths**:  
   - Ensure that the `edge_driver_path` is set to the location of the **Microsoft Edge WebDriver** on your computer.
   - Set the `output_file_path` to the desired location where you want the Excel file to be saved.

2. **Run the Script**:  
   Execute the script in your terminal or IDE.

   ```bash
   python dgda_allopathic_scraper.py
   ```

3. **Data Collection**:  
   The script will automatically scrape the data from the DGDA Allopathic Products page and save it in batches of 100 rows to the specified Excel file.

## Script Overview:

```python
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd
import time

# Set the path to the Edge WebDriver
edge_driver_path = r'C:\Users\Dell\Downloads\msedgedriver.exe'  # Update path here

# Set up Edge options
edge_options = Options()
edge_options.add_argument("--headless")  # Run headless Edge
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")

# Set up the Edge WebDriver
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# URL of the DGDA allopathic products page
url = "http://dgdagov.info/index.php/registered-products/allopathic"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as necessary

# Initialize an empty list to hold all data
all_data = []
row_count = 0  # Counter for rows collected

# Loop to handle pagination
while True:
    print("Collecting data from the current page...")

    # Find the table
    try:
        table = driver.find_element(By.ID, 'gridData')
    except Exception as e:
        print("Error finding the table:", e)
        break

    # Extract headers
    if not all_data:  # Only extract headers once
        headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
        print("Headers found:", headers)

    # Extract rows
    rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip the header row
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if cols:  # Check if the row has columns
            all_data.append([col.text for col in cols])
            row_count += 1  # Increment the row count

            # Save to Excel every 100 rows
            if row_count % 100 == 0:
                df = pd.DataFrame(all_data, columns=headers)
                output_file_path = r'C:\Users\Dell\Downloads\dgda_allopathic_products.xlsx'  # Output path
                df.to_excel(output_file_path, index=False)
                print(f"Saved {row_count} rows to Excel.")

    print(f"Collected {len(rows)} rows from this page.")

    # Check for the next page button
    try:
        next_button = driver.find_element(By.ID, 'gridData_next')
        if "disabled" in next_button.get_attribute("class"):
            print("No more pages to load.")
            break  # Exit the loop if the next button is disabled
        next_button.click()  # Click the next button
        time.sleep(5)  # Wait for the next page to load
    except Exception as e:
        print("No more pages or an error occurred:", e)
        break  # Exit the loop if no next button is found

# Check if any data was collected
if all_data:
    # Create a DataFrame
    df = pd.DataFrame(all_data, columns=headers)

    # Save the DataFrame to an Excel file if there are remaining rows
    if row_count % 100 != 0:  # Save if there are leftover rows
        output_file_path = r'C:\Users\Dell\Downloads\dgda_allopathic_products.xlsx'  # Output path
        df.to_excel(output_file_path, index=False)
        print(f"Saved remaining {row_count} rows to Excel.")

    # Display the DataFrame
    print("Data collection complete. Here are the first few rows:")
    print(df.head())
else:
    print("No data collected.")

# Close the driver
driver.quit()
```

## How the Script Works:

1. **Setup**:  
   - The **Edge WebDriver** is set up to run in headless mode, meaning it doesn't open a visible browser window.
   - The script navigates to the DGDA Allopathic Products page.

2. **Data Collection**:  
   - The script retrieves data from the product table on the page, including headers and rows.
   - It checks for a "Next" button to handle pagination and continues collecting data across multiple pages.

3. **Excel Export**:  
   - Every 100 rows, the data is written to an Excel file, ensuring that the script doesn't run into memory issues.
   - At the end of the script, all collected data is saved to a specified Excel file.

4. **Graceful Shutdown**:  
   - Once all pages are scraped, the browser is closed, and the program terminates.

## Troubleshooting:

- **WebDriver Version**: Ensure the version of `msedgedriver.exe` matches your installed version of Microsoft Edge.
- **Page Structure**: If the page structure changes, the script might need to be updated (e.g., changes in the table ID or pagination buttons).
- **Excel File Path**: Ensure you have write permissions to the directory where you are saving the Excel file.

---

This **README** provides a comprehensive overview and step-by-step instructions on using the script. If you have any further questions or issues, feel free to ask!
