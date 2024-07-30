from imports import *
from getcoord import get_coordinates


def main():
    # Path to your chromedriver
    chromedriver_path = "chromedriver.exe"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.google.com/maps/@32.8191173,-97.3554595,10z?hl=en&entry=ttu")
    sleep(1)

    def get_keyword_from_file():
        with open('place_and_keyword.txt', 'r') as file:
            lines = file.readlines()
            keyword = lines[1].strip()
            return keyword
            
    def get_place_from_file():
        with open('place_and_keyword.txt', 'r') as file:
            lines = file.readlines()
            place = lines[0].strip()
            return place

    def searchplace():
        # Locate the search box using its id
        place = driver.find_element(By.ID, "searchboxinput")
        locc = get_place_from_file()
        place.send_keys(locc)
        sleep(2)  # Added sleep to ensure the input is fully typed
        # Locate the search button using its id
        submit = driver.find_element(By.ID, "searchbox-searchbutton")
        submit.click()

    shop = []
    rating = []
    total_ratings = []
    type = []
    addr = []
    web = []
    number = []

    def findshopss():
        try:
            # Click the "nearby" button
            findshop = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[3]/button')
            findshop.click()
            sleep(5)  # Wait for the menu to open

            # Enter "vape" in the search field
            place = driver.find_element(By.ID, "searchboxinput")
            kw = get_keyword_from_file()
            place.send_keys(kw)
            sleep(1)

            # Click the search button
            submit = driver.find_element(By.ID, "searchbox-searchbutton")
            submit.click()
            sleep(5)  # Wait for the search results to load

            # Scroll to load more content
            scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
            last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

            while True:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                sleep(2)
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                if new_height == last_height:
                    break
                last_height = new_height

            # Collect shop elements
            All_shops = driver.find_elements(By.CLASS_NAME, "Nv2PK")
            print(f"Number of shops found: {len(All_shops)}")  # Debugging print

            for i in All_shops:
                try:
                    # Scroll the element into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", i)
                    ActionChains(driver).move_to_element(i).click().perform()
                    sleep(3)  # Allow time for the details to load

                    # Initialize values
                    href_value = "N/A"
                    contact = "N/A"
                    loca = "N/A"
                    rate = 'N/A'
                    review = "N/A"
                    stype = "N/A"

                    # For shop name
                    try:
                        shop_ = driver.find_element(By.CLASS_NAME, "DUwDvf.lfPIob")
                        shop_name = shop_.text
                        shop.append(shop_name)
                    except NoSuchElementException:
                        shop.append("N/A")

                    # For shop type
                    try:
                        All_shop_type = driver.find_element(By.CSS_SELECTOR, '.fontBodyMedium > span > span > button.DkEaL')
                        stype = All_shop_type.text
                    except NoSuchElementException:
                        pass
                    type.append(stype)

                    # For ratings
                    try:
                        All_shop_ratings = driver.find_element(By.CSS_SELECTOR, '.F7nice >span >span')
                        rate = All_shop_ratings.text
                    except NoSuchElementException:
                        pass
                    rating.append(rate)

                    # For total reviews
                    try:
                        All_shop_reviews = driver.find_element(By.CSS_SELECTOR, '.F7nice > span:nth-of-type(2) >span >span')
                        review = All_shop_reviews.text
                    except NoSuchElementException:
                        pass
                    total_ratings.append(review)

                    # For address
                    try:
                        All_shop_address = driver.find_element(By.CSS_SELECTOR, '.RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L > button[data-item-id="address"] > div.AeaXub > div.rogA2c >div.Io6YTe.fontBodyMedium.kR99db')
                        loca = All_shop_address.text
                    except NoSuchElementException:
                        pass
                    addr.append(loca)

                    # For website
                    try:
                        All_shop_website = driver.find_element(By.CSS_SELECTOR, '.RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L > a[data-item-id="authority"]')
                        href_value = All_shop_website.get_attribute('href')
                    except NoSuchElementException:
                        pass
                    web.append(href_value)

                    # For number
                    try:
                        All_shop_number = driver.find_element(By.CSS_SELECTOR, ".RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L > button[data-tooltip='Copy phone number'] > div.AeaXub > div.rogA2c > div.Io6YTe.fontBodyMedium.kR99db")
                        contact = All_shop_number.text
                    except NoSuchElementException:
                        pass
                    number.append(contact)

                except ElementClickInterceptedException:
                    print("Element click intercepted, retrying...")
                    sleep(2)
                    continue
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue

        except Exception as e:
            print(f"An error occurred in findshopss: {e}")

    searchplace()

    sleep(5)

    findshopss()

    driver.quit() 

    dic = {
        'shop': shop,
        'rating': rating,
        'total_ratings': total_ratings,
        'type': type,
        'address': addr,
        'website': web,
        'number': number
    }

    df = pd.DataFrame(dic)

    df.drop_duplicates(inplace=True)

    cord=(df['shop']+df['address']).tolist()

    lat, lon = get_coordinates(cord)
 
    df['latitude'] = lat
    df['longitude'] = lon

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    k= get_keyword_from_file()

    p=get_place_from_file()

    filename = f'output/scrape_{p}_{k}_{timestamp}.xlsx'
   
    df.to_excel(filename, index=False)

    return df
   
    