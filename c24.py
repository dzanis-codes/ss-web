## uzlabojumi - 
## 1. linkus varētu ņemt no sitemap, bet tad vajadzīgs spiest uz pogām par jaunākajiem
## 2. ja uzspiestu uz otrās dzīvokļu lapas, tad varētu ņemt retāk
## 3. sludinajumu kategorijas sale/rent varētu ņemt no lapas
## 4. sadalīt plot tekstu pareizi
## 5. var mēģināt vērt katru sludinajumu no pilnā sitemap vaļā un saglabāt arī vairāk info

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys
import sqlite3

driver = webdriver.Firefox()
conn = sqlite3.connect('result01c24.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()

link_list = ('https://www.city24.lv/en/list/sale/rent/houses?str=2&lang=en&c=LV&tt=1&it=8&ord=sort-date-desc&fr=0', 'https://www.city24.lv/en/list/sale/rent/apartments?str=2&lang=en&c=LV&tt=1&it=18&ord=sort-date-desc&fr=0')


def glabat_slud(link, type):
    driver.get(link)
    time.sleep(4)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    #g_data = soup.find_all("div", {"class": "results resultList"})


    h_data = soup.find_all("li", {"class": "new result regular"})
    for count in range(50):
        ad_link = h_data[count].find("a")['href']
        img_link = h_data[count].find("img")['src']
        
        adrese_tag = h_data[count].find("a", {"class": "addressLink"})
        adrese = adrese_tag.text
        ad_id = adrese_tag["name"]

        cena_tag = h_data[count].find("div", {"class": "price"})
        cena = cena_tag.text
        
        cena_m2_tag = h_data[count].find("div", {"class": "price_sqrm"})
        cena_m2 = cena_m2_tag.text

        citsinfo = h_data[count].find_all("div", {"class": "result_content"})
        for item in citsinfo:
            apraksts_tag = item.find("div", {"class": "promo"})
            if apraksts_tag != None:
                apraksts = apraksts_tag.text
            else:
                apraksts = "na"
        platiba = citsinfo[0].find_all('li')[0].text
        istabas = citsinfo[0].find_all('li')[1].text
        stavi = citsinfo[0].find_all('li')[2].text
        
        if type == 0:
          estate_type = "House"
        else:
          estate_type = "Appartment"
        ts = time.gmtime()
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        print(" adrese: "+ adrese + " ad id: "+ad_id + "cena:  "+cena+ "platiba, istabas un stavi" + platiba + istabas+ stavi, stamp)
        sql_entry = (str(ad_id), str(apraksts), str(stavi), str(adrese), str(platiba), str(cena), str(cena_m2), str(ad_link), "c24", estate_type, str(istabas), stamp) 
        ## db file structure: INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()

link = 0
while link != 2:
    try:
        driver.get(link_list[link])
        time.sleep(4)
        glabat_slud(link_list[link], link)
        link += 1
    except: Exception
        f = open('log.txt', 'a')
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        liste = (saraksts_darij[darijuma_veids], saraksts_veids[ipasuma_veids], lpp)
        f.write('\n %s \n' % str(timestamp))
        f.write('\n error atverot linku nr.: '.join(str(link)))
        f.close()
        pass
sys.exit()
