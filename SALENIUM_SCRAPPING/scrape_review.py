from imports import *

def run_review_scrape(placee):
    chromedriver_path = "chromedriver.exe"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.google.com/maps/@32.8191173,-97.3554595,10z?hl=en&entry=ttu")
    sleep(1)

    def searchplace(placee):
        # Locate and clear the search box, then search
        place = driver.find_element(By.ID, "searchboxinput")
        place.clear()
        sleep(2)
        place.send_keys(placee)
        sleep(2)
        submit = driver.find_element(By.ID, "searchbox-searchbutton")
        submit.click()
        sleep(4)

        try:
            shop = driver.find_element(By.CLASS_NAME, "hfpxzc")
            shop.click()
            sleep(2)
        except Exception as e:
            pass

        try:
            # Navigate to the reviews section
            review_nav = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)')
            review_nav.click()
            sleep(3)
        except Exception as e:
            pass

        try:
            sort = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Sort reviews"]')
            sort.click()
            sleep(3)
        except Exception as e:
            pass
        
        try:
            new = driver.find_element(By.CSS_SELECTOR, '#action-menu > div:nth-child(2)')
            new.click()
            sleep(4)
        except Exception as e:
            pass

        # Scroll to load more content
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        
        scroll_count = 1
        max_scrolls = 5
        
        while scroll_count < max_scrolls:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            sleep(2)
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if new_height == last_height:
                break
            last_height = new_height
            scroll_count += 1

        # Extract review data
        review_boxes = driver.find_elements(By.CLASS_NAME, "jJc9Ad")
        names = []
        times = []
        user_comments = []
        rating_stars = []

        for box in review_boxes:
            try:
                name = box.find_element(By.CLASS_NAME, "d4r55").text
            except:
                name = "N/A"
            names.append(name)
            
            try:
                time_ago = box.find_element(By.CLASS_NAME, "rsqaWe").text
            except:
                time_ago = "N/A"
            times.append(time_ago)

            try:
                ratings = box.find_element(By.CLASS_NAME, "kvMYJc").get_attribute("aria-label")
            except:
                ratings = "N/A"
            rating_stars.append(ratings)
            
            try:
                li_review = box.text.split('\n')[9:]
                li_review = [line for line in li_review if line not in ['\ue8dc', '\ue80d']]
                
                if li_review:
                    li_review = li_review[:-2]
                else:
                    li_review.append("BLANK")

                li_review = [i.split('Translated by Google')[0].strip() if "Translated by Google" in i else i for i in li_review]
                user_comment = ' '.join(li_review)
            except:
                user_comment = "N/A"
            user_comments.append(user_comment)

        driver.quit()

        # Save to Excel
        data = {
            "Shop_Name": placee.split(",")[0],
            "Name": names,
            "Time_Of_Comment": times,
            "Rating_Stars": rating_stars,
            "Review_Comment": user_comments
        }
        
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'output_reviews/{placee.split(",")[0]}_reviews_{timestamp}.xlsx'
        df.to_excel(filename, index=False)

    searchplace(placee)
