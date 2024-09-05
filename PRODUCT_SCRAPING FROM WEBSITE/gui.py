# gui.py
import streamlit as st
from app import process_website  # Import the function from app.py

# Streamlit UI Configuration
st.set_page_config(page_title="Web Scraper Tool", page_icon=":mag:", layout="centered")

# Application Title and Description
st.title("🕸️ Web Scraper Tool")
st.write("""
Welcome to the Web Scraper Tool! This application allows you to scrape products and other information from websites.
Simply enter a URL and click 'Submit' to start scraping. The scraped data will be saved in a CSV file.
""")

# Display an Image for Web Scraping Visualization
st.write("---")  # Horizontal line separator
st.subheader("🖼️ Web Scraping Visualization")

# Display Image (Ensure 'scrap.png' is in the same directory as this script or provide the correct path)
st.image("scrap.png", caption="Web Scraping in Action", use_column_width=True)

# URL Input Section
st.write("---")  # Horizontal line separator
st.subheader("🔗 Enter Website URL to Scrape")
url = st.text_input("Enter the website URL you want to scrape:", "")

# Button to Submit and Start Scraping
if st.button("Submit"):
    if url:
        try:
            # Call the function to process the website
            process_website(url)
            st.success(f"✅ Scraping completed for {url}. Check the output folder for the CSV file.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid URL.")

# Footer Section
st.write("---")  # Horizontal line separator
st.write("Developed by Apil | Powered by Streamlit & Selenium")
