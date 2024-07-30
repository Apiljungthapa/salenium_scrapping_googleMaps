from imports import *

def get_coordinates(li):
        
        chromedriver_path = "chromedriver.exe"
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.google.com/maps/@32.8191173,-97.3554595,10z?hl=en&entry=ttu")

        latitude = []
        longitude = []

        def searchplace(li):

            for location in li:
                try:
                
                    # Locate the search box and clear previous input
                    place = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
                    place.clear()
                    place.send_keys(location)

                    # Locate the search button and click it
                    submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "searchbox-searchbutton")))
                    submit.click()

                    sleep(3)
                    
                    current_url = driver.current_url
                    parsed_url = urlparse(current_url)
                    
                    # Extract coordinates from URL
                    path = parsed_url.path.split('/')
                    coordinates = [part for part in path if '@' in part]

                    if coordinates:
                        lat_lng = coordinates[0].split('@')[1].split(',')[0:2]
                        latitude.append(lat_lng[0])
                        longitude.append(lat_lng[1])
                    else:
                        latitude.append("N/A")
                        longitude.append("N/A")

                except Exception as e:
                    print(f"An error occurred while searching for {location}: {e}")
                    latitude.append("N/A")
                    longitude.append("N/A")

        searchplace(li)

        driver.quit()

        return latitude, longitude

        

