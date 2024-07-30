from imports import *

def email_process(df):

    df['emails']=None
    
    platforms = ['facebook', 'instagram', 'twitter', 'linkedin', 'pinterest', 'snapchat', 'tiktok', 'youtube', 'whatsapp', 'reddit']

    filter = [ i for i in df['website'].dropna().astype(str) if not any(platform in i for platform in platforms)]

    # Replace with the path to your ChromeDriver executable
    service = Service('chromedriver.exe')
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service)

    all_emails = []


    def extract_emails_from_website(urls):
            for url in urls:
                try:
                    driver.get(url)
                    # Adding a small delay to ensure the page loads completely
                    time.sleep(3)
                    
                    # Get page source
                    page_source = driver.page_source
                    
                    # Regular expression to find email addresses
                    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
                    emails = set(email_pattern.findall(page_source))

                    if not emails:
                        all_emails.append("N/A")
                    else:
                        femails=[i for i in emails if "sentry" not in i and "wixpress" not in i and "jpg" not in i ]
                        all_emails.append(femails)

                
                except WebDriverException as e:
                    all_emails.append("N/A") 
    

    emails=extract_emails_from_website(filter)

    # Convert each inner list to a string, and handle individual strings
    converted_list = [', '.join(sublist) if isinstance(sublist, list) else sublist for sublist in all_emails]

    # Quit the driver
    driver.quit()

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    df.loc[df['website'].isin(filter),'emails'] = converted_list

    filename = f'output_with_emails/scrape_with_mails_{timestamp}.xlsx'
   
    df.to_excel(filename, index=False)

 