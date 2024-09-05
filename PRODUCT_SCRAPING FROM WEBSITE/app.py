# app.py
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Set up Chrome WebDriver with enhanced error handling and specified port
def setup_selenium_driver():  
    try:
        service = Service("chromedriver.exe")  # Update the path to your ChromeDriver executable
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")  # Disable notifications for clean extraction
        chrome_options.add_argument("--start-maximized")  # Start maximized for full-page view
        chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
        chrome_options.add_argument("--allow-running-insecure-content")  # Allow insecure content
        # Remove headless mode for debugging; add "--headless" back for headless mode
        # chrome_options.add_argument("--headless")  # Run in headless mode to save resources

        # Initialize the WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Failed to initialize Chrome WebDriver: {e}")
        return None

# Initialize the WebDriver
driver = setup_selenium_driver()
if driver is None:
    exit("WebDriver could not be initialized. Exiting...")

# Function to extract content from a page
def extract_content_from_page(url):
    try:
        driver.get(url)
        time.sleep(3)  # Adjust based on website's loading speed
        
        # Handle pop-ups or age verification if present
        try:
            enter_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Enter") or contains(text(), "Agree")]'))
            )
            enter_button.click()
            time.sleep(2)
        except:
            print("No pop-up or age verification found.")
        
        # Extract main content
        page_content = ''
        elements = driver.find_elements(By.XPATH, "//*[not(self::script or self::style or self::noscript)]")
        for element in elements:
            text = element.text.strip()
            if text:
                page_content += text + "\n"
                
        return page_content
    except Exception as e:
        print(f"Failed to extract content from {url}: {e}")
        return ""

# Function to find all internal links on a page
def find_all_links_on_page():
    try:
        # Find all anchor tags with href attributes
        links = driver.find_elements(By.XPATH, "//a[@href]")
        all_links = [link.get_attribute("href") for link in links]
        # Filter out links that are external or empty
        all_links = [link for link in all_links if link and link.startswith("http")]
        return all_links
    except Exception as e:
        print(f"Error finding links: {e}")
        return []

# Main function to scrape the website
def scrape_website(website_url):
    # Set to keep track of visited links to avoid duplicates
    visited_links = set()
    # List to keep all content
    all_content = []

    # Start with the home page
    links_to_visit = [website_url]

    while links_to_visit:
        current_url = links_to_visit.pop(0)
        
        if current_url not in visited_links:
            print(f"Visiting: {current_url}")
            visited_links.add(current_url)

            # Extract content from the current page
            content = extract_content_from_page(current_url)
            if content:
                all_content.append(content)
            
            # Save extracted content to a text file
            with open('website_full_content.txt', 'a', encoding='utf-8') as file:
                file.write(f"\n\nContent from {current_url}:\n")
                file.write(content)
            
            # Find all new links on the current page and add them to the list of links to visit
            new_links = find_all_links_on_page()
            for link in new_links:
                if link not in visited_links and link.startswith(website_url):  # Only add internal links
                    links_to_visit.append(link)
    
    return all_content

# Function to extract products from the page content using LLM
def extract_products(page_data):
    prompt_template = PromptTemplate.from_template(""" Analyze the following content scrap from a website to identify products related to the specified categories. Extract only those products that are found directly in the provided content and match the categories below. If no products matching the categories are found, return "No products found."

    {contents}

    ### Categories to identify:
    - Vapes
    - Smokes
    - Cigars
    - Tobacco products
    - Geekbar
    - Apparels
    - Candies and bars
    - Biotany products
    - Health and beauty care
    - Household items
    - Lighters and fuels
    - Nicotine pouches
    - Rolling papers and gums
    - Wraps
    - Electronics
    - Salts
    - Disposable

    ### Instructions:
    1. Extract only those products from the content that match the categories listed above. 
    2. Do not include example products unless they are found directly in the content. 
    3. If no matching products are found in the content, return "No products found."

    ### Output Format:
    - List all identified products in plain text format, one product per line.
    - If no products are identified, return "No products found."

    ### (LIST FORMAT NO PREAMBLE)
    """)

    # Initialize LLM
    llm = ChatGroq(
        temperature=0.5, 
        groq_api_key='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', 
        model_name="llama-3.1-70b-versatile"
    )
    
    # Run the LLM chain with the page content
    chain = prompt_template | llm
    response = chain.invoke({'contents': page_data})

    # Return the cleaned response content
    cleaned_string = response.content.replace('\n', '').replace('-', '')
    product_list = [item.strip() for item in cleaned_string.split(',') if item.strip()]
    
    return product_list

# Function to save products to a single CSV file for all URLs
def save_to_csv(url, product_list):
    # Create a DataFrame where each product is a new row with the website link repeated
    df = pd.DataFrame({'Website': [url] * len(product_list), 'Product': product_list})

    # Define output file path for the single CSV file
    output_file_path = r"C:\Users\Apil Thapa\Desktop\SCRAP_PRODUCTS\output_files\scraped_products.csv"

    # Check if the CSV file already exists
    if os.path.exists(output_file_path):
        # If it exists, append without writing the header
        df.to_csv(output_file_path, mode='a', header=False, index=False)
    else:
        # If it does not exist, create it and write the header
        df.to_csv(output_file_path, mode='w', header=True, index=False)

    print(f"Data appended to '{output_file_path}' successfully!")

# Main function to run the full process
def process_website(url):
    all_content = scrape_website(url)  # Scrape all content from the website
    if all_content:
        # Combine all content into a single string for LLM processing
        combined_content = "\n\n".join(all_content)
        products = extract_products(combined_content)
        save_to_csv(url, products)
    else:
        print("Failed to fetch page content; no CSV generated.")
