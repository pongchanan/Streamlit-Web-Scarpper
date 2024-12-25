import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

st.markdown("<h1 style='text-align: center'>Web scrapper</h1>", unsafe_allow_html=True)

with st.form("Search"):
    keyword = st.text_input("Enter your keyword")
    search = st.form_submit_button("Search")
    if search:
        # Set up Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        url = f"https://unsplash.com/s/photos/{keyword}"
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)

        # Scrape the required content
        rows = driver.find_elements(By.CLASS_NAME, "ripi6")
        
        # Close the browser
        driver.quit()
