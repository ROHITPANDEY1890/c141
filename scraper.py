from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import requests

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

planets_data = []
new_planets_data=[]
# Define Exoplanet Data Scrapping Method
def scrape_more_data(hyperlink):
    try: 
        page = requests.get(hyperlink) 
        soup = BeautifulSoup(page.content, "html.parser") 
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}): 
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags: 
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]) 
                except: 
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


def scrape():
    planets_data=[]
    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
        soup=BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index, li_tag in enumerate(li_tags): 
                if index == 0: 
                    temp_list.append(li_tag.find_all("a")[0].contents[0]) 
                else: 
                    try:
                        temp_list.append(li_tag.contents[0]) 
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planets_data.append(temp_list)
    browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]
    with open("scraper_2.csv","w") as f:
        csvwriter = csv.writer(f) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(planets_data)

scrape()

        ## ADD CODE HERE ##
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
for index, data in enumerate(planets_data):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")

        
# Calling Method    


# Define pandas DataFrame   
final_planet_data=[] 
for index, data in enumerate(planets_data):
    new_planets_data_element = new_planets_data[index] 
    new_planets_data_element=[elem.replace("\n","") for elem in new_planets_data_element] 
    new_planets_data_element=new_planets_data_element[:7] 
    final_planet_data.append(data+new_planets_data_element)


# Convert to CSV
with open("final.csv","w") as f:
        csvwriter = csv.writer(f) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(final_planet_data)
        
    


