from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd
import time

# Set the path to the Edge WebDriver
edge_driver_path = r'C:\Users\Hamada Salim Trd\OneDrive\Desktop\Pharmecy Data scap by abdullah\msedgedriver.exe'  # Update this path

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
                output_file_path = r'C:\Users\Hamada Salim Trd\OneDrive\Desktop\Pharmecy Data scap by abdullah\dgda_allopathic_products.xlsx'
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
        output_file_path = r'C:\Users\Hamada Salim Trd\OneDrive\Desktop\Pharmecy Data scap by abdullah\dgda_allopathic_products.xlsx'
        df.to_excel(output_file_path, index=False)
        print(f"Saved remaining {row_count} rows to Excel.")

    # Display the DataFrame
    print("Data collection complete. Here are the first few rows:")
    print(df.head())
else:
    print("No data collected.")

# Close the driver
driver.quit()