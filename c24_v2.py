import time
from bs4 import BeautifulSoup
import sys
import sqlite3
import requests
import traceback
from selenium import webdriver
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
#options.add_argument('--window-size=800,400')  
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

path = '/LBData/jaunakie_dati/result01c24.db'
conn = sqlite3.connect(path) 
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp)''')
# Save (commit) the changes
conn.commit()


link_list = ('https://www.city24.lv/real-estate-search/houses-for-sale/date=today', 'https://www.city24.lv/real-estate-search/apartments-for-sale/date=today', 'https://www.city24.lv/real-estate-search/houses-for-rent/date=today', 'https://www.city24.lv/real-estate-search/apartments-for-rent/date=today')


def glabat_slud(link, type):
    print(link)
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options = options)
    #print("..4")
 
    #driver.get(link)
    time.sleep(6)
    #print("..5")
    #a = driver.find_element_by_css_selector('[id="onetrust-accept-btn-handler"]')
    #print(a)
    #driver.find_element_by_css_selector('[id="onetrust-accept-btn-handler"]').click()
    #time.sleep(3)
    #print("..6")
    #b = driver.find_element_by_css_selector('[class="select__value"]')
    #print(b)
    #driver.find_element_by_css_selector('[class="select__value"]').click()
    #print("..7")
    #time.sleep(3)
    #driver.find_element_by_css_selector('[value = "datePublished-desc"]').click()
    #time.sleep(5)
    #print("..8")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print("..9")
    g_data = soup.find_all("div", {"class": "object object--list object--result"})
    
    #print(len(g_data))
    print("..")


    for count in range(len(g_data)):
        ad_link = g_data[count].find("a")['href']

        
        adrese_tag = g_data[count].find("a", {"class": "object__location"})
        #print(adrese_tag)
        print("3")
        if adrese_tag == None:
            adrese = "na"

           
        else:
            street = adrese_tag.find("h3", {"class": "object__address"}).text
            region = adrese_tag.find("div", {"class": "object__area"}).text
            #adrese = adrese_tag.text
            adrese = str(street) + "; " + str(region)
        print(adrese)

        cena_tag = g_data[count].find("div", {"class": "object-price__main-price"})
        cena_c = cena_tag.text
        cena = unicodedata.normalize("NFKD", cena_c)
        print(cena)
        
        cena_m2_tag = g_data[count].find("div", {"class": "object-price__m2-price"})
        if cena_m2_tag == None:
            cena_m2 = "na"
        else:
            cena_m2_c = cena_m2_tag.text
            cena_m2 = unicodedata.normalize("NFKD", cena_m2_c)
        citsinfo = g_data[count].find("div", {"class": "object__slogan"})
        if citsinfo == None:
            apraksts = "na"  
        else:
            apraksts = citsinfo.text

        check_platiba = g_data[count].find_all('ul')[0].text
        if "m" in check_platiba: 
            platiba = g_data[count].find_all('li')[0].text
        else:
            platiba = "na"

        main_features = g_data[count].find_all('ul')[0]
        #atrodam stavus
        if main_features.find("span", {"class": "icon icon-stairs"}) == None:
            stavi = "na"
        else:
            stavi = main_features.find("span", {"class": "icon icon-stairs"}).parent.text

        #atrodam istabas
        if main_features.find("span", {"class": "icon icon-door"}) == None:
            istabas = "na"
        else:
            istabas = main_features.find("span", {"class": "icon icon-door"}).parent.text

        ad_id = "na"
        if type == 0:
            estate_type = "House for sale"
        elif type == 1:
            estate_type = "Appartment for sale"
        elif type == 2:
            estate_type = "House for rent"
        else:
            estate_type = "Appartment for rent"
        ts = time.gmtime()
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        print(" adrese: ", adrese, " ad id: ",ad_id, "cena:  ", cena, "platiba, istabas un stavi", platiba, istabas, stavi, stamp)
        sql_entry = (str(ad_id), str(apraksts), str(stavi), str(adrese), str(platiba), "land?", str(cena), str(cena_m2), str(ad_link), "c24", estate_type, str(istabas), stamp) 
        ## db file structure: INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()
        print(sql_entry)

#main
link = 0
while link != 4:
    try:
        #print("2")
        glabat_slud(link_list[link], link)
        link += 1
    except Exception as e:
        path2 = '/LBApp_log/errorlog_c24.txt'
        f = open(path2, 'a+')
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        f.write('\n %s \n' % str(timestamp))
        f.write('\n %s \n' % e)
        tb = traceback.TracebackException.from_exception(e)
        f.write('\n'.join(tb.stack.format()))        
        f.write('\n error atverot linku nr.: '.join(str(link)))
        f.close()
        time.sleep(10)
        pass
sys.exit()
