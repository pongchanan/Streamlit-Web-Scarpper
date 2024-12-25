import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

st.set_page_config(
    page_title="Web scrapper",
    page_icon="👻"
)

st.markdown("<h1 style='text-align: center'>Web Scraper</h1>", unsafe_allow_html=True)

# Initialize session state for search results
if "image_urls" not in st.session_state:
    st.session_state.image_urls = []
if "link_urls" not in st.session_state:
    st.session_state.link_urls = []

with st.form("Search"):
    keyword = st.text_input("Enter your keyword")
    search = st.form_submit_button("Search")

    if search:
        # Clear previous results
        st.session_state.image_urls = []
        st.session_state.link_urls = []

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
        try:
            rows = driver.find_elements(By.CLASS_NAME, "I7e4t")  # Adjust if this class changes
            for row in rows:
                figures = row.find_elements(By.TAG_NAME, 'figure')
                for figure in figures:
                    try:
                        anchor = figure.find_element(By.TAG_NAME, 'a')
                        st.session_state.link_urls.append(anchor.get_attribute('href'))
                        img = figure.find_elements(By.TAG_NAME, 'img')[1]  # Adjust index as needed
                        img_url = img.get_attribute('src')
                        st.session_state.image_urls.append(img_url)
                    except Exception:
                        pass
        except Exception as e:
            st.error(f"An error occurred: {e}")

        driver.quit()
        
        if not st.session_state.image_urls:
            st.write("No images found. Please try a different keyword.")

# Display images with clickable links
if st.session_state.image_urls:
    col1, col2 = st.columns(2)
    st.write(f"Found {len(st.session_state.image_urls)} images for the keyword '{keyword}'")
    for counter, url in enumerate(st.session_state.image_urls):
        if counter % 2 == 0:
            col1.image(url)
            col1.markdown(
                f"<a href='{st.session_state.link_urls[counter]}' target='_blank'>Download Image</a>", 
                unsafe_allow_html=True
            )
        else:
            col2.image(url)
            col2.markdown(
                f"<a href='{st.session_state.link_urls[counter]}' target='_blank'>Download Image</a>", 
                unsafe_allow_html=True
            )
