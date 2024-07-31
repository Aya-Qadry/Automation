from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By

def start_search(url, brand):
    driver = webdriver.Chrome()

    try:
        driver.get(url)

            # wait for the search to be visible : 
        search_tool = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "SearchText"))
        )

        # ENter the brand name and submit : 

        search_tool.send_keys(brand)
        search_tool.send_keys(Keys.RETURN)

        time.sleep(15)

        # Find and click the link
        link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[_ngcontent-c8]"))
        )
        link.click()

        # Wait for the new page to load
        time.sleep(10)

    #fetch the current url containing the data i need : 
        return driver.page_source

    except Exception as e:
        print(e)
    finally:
        driver.quit()

def brand_info(source):
    # get the page's source code and create an bs object : 

    soup = BeautifulSoup(source, 'html.parser')

    fiche = soup.find('div', class_='fiche')

    if fiche:
        extracted_data = {}
        table = fiche.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    extracted_data[key] = value

        return extracted_data
    else:
        return "Brand information couldn't be found"

def main():
    url = "https://www.directinfo.ma/"
    brand = "ESTHECARE"

    source = start_search(url, brand)

    if source:
        results = brand_info( source)
        print(f"Extracted data: {results}")
    else:
        print("Search failed or no results found.")

if __name__ == "__main__":
    main()