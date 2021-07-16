

import time
from bs4 import BeautifulSoup
import sys
import sqlite3
import requests
import traceback
from selenium import webdriver
import unicodedata

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# open it, go to a website, and get results




conn = sqlite3.connect('result01c24.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp)''')


# Save (commit) the changes
conn.commit()
link_list = ('https://www.city24.lv/en/list/sale/rent/houses?str=2&lang=en&c=LV&tt=1&it=8&ord=sort-date-desc&fr=0', 'https://www.city24.lv/en/list/sale/rent/apartments?str=2&lang=en&c=LV&tt=1&it=18&ord=sort-date-desc&fr=0')


def glabat_slud(link, type):
    print(link)
    driver = webdriver.Chrome('chromedriver',options=options)
 
    driver.get(link)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    g_data = soup.find_all("div", {"class": "object object--list object--result"})
    
    print(len(g_data))
    print("..")
    print(g_data[1])

    for count in range(len(g_data)):
        ad_link = g_data[count].find("a")['href']

        
        adrese_tag = g_data[count].find("a", {"class": "object__location"})
        #print(adrese_tag)
        print("3")
        adrese = adrese_tag.text
        print(adrese)
        #šo var sadalīt divos lielumos
       

        cena_tag = g_data[count].find("div", {"class": "object-price__main-price"})
        cena_c = cena_tag.text
        cena = unicodedata.normalize("NFKD", cena_c)
        print(cena)
        
        cena_m2_tag = g_data[count].find("div", {"class": "object-price__m2-price"})
        cena_m2_c = cena_m2_tag.text
        cena_m2 = unicodedata.normalize("NFKD", cena_m2_c)
        citsinfo = g_data[count].find("div", {"class": "object__slogan"})
        apraksts = citsinfo

        platiba = g_data[count].find_all('ul')[0].text
        istabas = g_data[count].find_all('li')[1].text
        if len(g_data[count].find_all('li')) > 2:
          stavi = g_data[count].find_all('li')[2].text
        else:
          stavi = "1"
        ad_id = "na"
        if type == 0:
          estate_type = "House"
        else:
          estate_type = "Appartment"
        ts = time.gmtime()
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        print(" adrese: "+ adrese + " ad id: "+ad_id + "cena:  "+cena+ "platiba, istabas un stavi" + platiba + istabas+ stavi, stamp)
        sql_entry = (str(ad_id), str(apraksts), str(stavi), str(adrese), str(platiba), "land?", str(cena), str(cena_m2), str(ad_link), "c24", estate_type, str(istabas), stamp) 
        ## db file structure: INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()
        print(sql_entry)

print("1")
link = 0
while link != 2:
    try:
        print("2")

        glabat_slud(link_list[link], link)
        link += 1
    except Exception as e:
        f = open('errorlog_c24.txt', 'a+')
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
