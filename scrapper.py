import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

st.markdown("<h1 style='text-align: center'>Web Scraper</h1>", unsafe_allow_html=True)

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

        # Construct the URL
        url = f"https://unsplash.com/s/photos/{keyword}"
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)

        # Scrape image URLs
        image_urls = []
        try:
            # Locate all image elements
            rows = driver.find_elements(By.CLASS_NAME, "I7e4t")  # Adjust if this class changes
            for row in rows:
                figures = row.find_elements(By.TAG_NAME, 'figure')
                for figure in figures:
                    try:
                        # Locate the image element
                        img = figure.find_elements(By.TAG_NAME, 'img')[1]  # Adjust index as needed
                        # Extract the highest resolution URL from the 'src' attribute
                        img_url = img.get_attribute('src')  
                        image_urls.append(img_url)
                    except Exception:
                        pass  # Skip if the image isn't found
        except Exception as e:
            st.error(f"An error occurred: {e}")

                
        # Close the browser
        driver.quit()

        # Display results in Streamlit
        if image_urls:
            st.write(f"Found {len(image_urls)} images for the keyword '{keyword}'")
            for url in image_urls:
                st.image(url, width=300)  # Display the image in Streamlit
        else:
            st.write("No images found. Please try a different keyword.")
