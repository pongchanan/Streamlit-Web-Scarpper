from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

website = 'https://www.adamchoi.co.uk/overs/detailed'

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (needed for some environments)

# Initialize the WebDriver with headless options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the website
driver.get(website)

# Wait for the page to load
time.sleep(2)

# Click the "All matches" button
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

# Select Spain from the dropdown
dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Spain')

time.sleep(2)

# Lists to store scraped data
date = []
home_team = []
score = []
away_team = []

# Find all rows in the table
matches = driver.find_elements(By.TAG_NAME, 'tr')

# Loop through each match row
for match in matches:
    try:
        # Try to get the text from each column
        d = match.find_element(By.XPATH, './td[1]').text
        ht = match.find_element(By.XPATH, './td[2]').text
        s = match.find_element(By.XPATH, './td[3]').text
        at = match.find_element(By.XPATH, './td[4]').text
        
        # Add to list
        date.append(d)
        home_team.append(ht)
        score.append(s)
        away_team.append(at)
    except Exception as e:
        break

# Quit the driver after scraping
driver.quit()

# Create a DataFrame
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})

# Save the data to a CSV file
df.to_csv('football_data.csv', index=False)
print(df)
