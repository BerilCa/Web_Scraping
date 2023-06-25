from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver')
driver = webdriver.Chrome(service=servis, options=opsi)

link = "https://www.genericdrugscan.com/jan-aushadhi-stores/"
driver.get(link)
time.sleep(5)

driver.save_screenshot("home.png")
content = driver.page_source

data = BeautifulSoup(content, 'html.parser')

table = data.find('table')
rows = table.find_all('tr')

# Initialize the data_list
data_list = []

# Print state
for row in rows:
    cells = row.find_all('td')
    if cells:  # Skip header row
        state = cells[0].find('a').text
        print("state: ", state)

        link = cells[0].find('a')['href']  # Mendapatkan URL tautan
        driver.get(link)  # Mengklik tautan

        time.sleep(7)
        content = driver.page_source
        data = BeautifulSoup(content, 'html.parser')

        table = data.find('table')
        rows = table.find_all('tr')

        # Print district
        for row in rows:
            cells = row.find_all('td')
            if cells:  # Skip header row
                district = cells[0].find('a').text
                print("District: ", district)

                # info store
                link = cells[0].find('a')['href']  # Mendapatkan URL tautan
                driver.get(link)  # Mengklik tautan

                time.sleep(7)
                content = driver.page_source
                data = BeautifulSoup(content, 'html.parser')

                i = 1
                for area in data.find_all('table'):
                    # print("Nomor: ", i)
                    nama = area.find('b').get_text() if area.find('b') else "Not found"

                    store_code_element = area.find('td', string='Store Code')
                    store_code = store_code_element.find_next_sibling('td').text if store_code_element else "Not found"

                    addres_element = area.find('td', string='Address')
                    addres = addres_element.find_next_sibling('td').text if addres_element else "Not found"

                    district_element = area.find('td', string='District')
                    district = district_element.find_next_sibling('td').text if district_element else "Not found"

                    state_element = area.find('td', string='State')
                    state = state_element.find_next_sibling('td').text if state_element else "Not found"

                    pin_code_element = area.find('td', string='Pin Code')
                    pin_code = pin_code_element.find_next_sibling('td').text if pin_code_element else "Not found"

                    contact_person_element = area.find('td', string='Contact Person')
                    contact_person = contact_person_element.find_next_sibling('td').text if contact_person_element else "Not found"

                    contact_detail_element = area.find('td', string='Contact Detail')
                    contact_detail = contact_detail_element.find_next_sibling('td').text if contact_detail_element else "Not found"

                    status_element = area.find('td', string='Status')
                    status = status_element.find_next_sibling('td').text if status_element else "Not found"

                    i += 1
                    print("Store: ", nama)
                    print("Store code: ", store_code)
                    print("Address: ", addres)
                    print("District: ", district)
                    print("State: ", state)
                    print("Pin Code: ", pin_code)
                    print("Contact Person: ", contact_person)
                    print("Contact Detail: ", contact_detail)
                    print("Status: ", status)
                    print("________________________________")

                    # Create dictionary for storing data
                    data_dict = {
                        'store': nama,
                        'store code': store_code,
                        'address': addres,
                        'state': state,
                        'pin code': pin_code,
                        'district': district,
                        'contact person': contact_person,
                        'contact detail': contact_detail,
                        'status': status
                    }

                    # Append the dictionary to the data_list
                    data_list.append(data_dict)

                # Go back to the previous page
                driver.back()

driver.quit()

# Create a DataFrame from the data_list
df = pd.DataFrame(data_list)

# Save DataFrame to a CSV file
df.to_csv('scraped_data.csv', index=False)
