## pedejas izmaiņas:
## 1. izņēmu csv rakstīšanu ārā
## 2. pamainīšu datubāzi un šo jāpalaiž kā papildu jaunu event paralēli vecajam... ja nu kaut kas nobrūk
import sys
import requests
import time
from bs4 import BeautifulSoup
import sqlite3

ts = time.gmtime()

## Datubāzei vairāki papildinājumi: pielikt kolonnu "saite", kolonnu "darijums - ar opciju pardod/izire", kolonnu "avots", kur bus ss.com, kolonnu "nek.veids" 
## ar attieciguiem mainigajiem dzivoklis, maja, zeme, vasarnica, telpas, biroji
## un tad vēl jaunas kolonnas zemes pl. (kur ir m2 vai ha vai na) 
conn = sqlite3.connect('result02.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()

## Tagad jāizveido divi saraksta mainigie - sell/hand-over; telpu saraksts
## Katram ir savs kolonnu skaits un informacija 

saraksts_darij = ("sell", "hand-over")
saraksts_veids = ("flats", "homes-summer-residences", "farms-estates", "premises", "offices")
        
## šeit seko lapu izskaitīšana 
## vai to vajag katram veidam? Laikam, ja gribu vienu kodu visām darbībām

url = "https://www.ss.com/lv/real-estate/flats/today-2/sell/
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

## tiek atlasitas visas tabulas
tables = soup.findAll('table')

#tiek ieguts sludinajumu skaits
slud_skaits = tables[1].find_all("option")[2].get_text()
skaits_n = slud_skaits.split()[-1]

#lpp skaits ir ar uzviju, un tad ir dublikati
lpp_skaits = round(int(skaits_n) / 30) + 4


## tad jaabuut funkcijai kas iteree cauri visaam lapaam
## shai funkcijai divi papildinajumi:
## 1. papildinajums ir mainigais vai sell/handover - maina tikai adresi
## 2. papildinajums ir mainigais par ni tipu - mainas adrese, kolonnas atzimejama informacija
def ss_scraping(lpp):
    url = "https://www.ss.com/lv/real-estate/flats/today-2/sell/page"+ str(lpp)+".html"
    
    ## Tālāk seko errorchecking sadaļa pārbaudot ss.com darbību
    ## --C1-- Nepieciešams uzlabot pievienojot error logging
    while True:
        try:
            r = requests.get(url)
            break
        except requests.exceptions.RequestException:
            time.sleep(300)

    soup = BeautifulSoup(r.content, 'html.parser')
    
    ## tiek atlasitas visas tabulas
    tables = soup.findAll('table')

    # interesanta parasti ir piekta tabula
    tablex = tables[4]
    
    # tiek atlasitas visas rindas tajaa tabulaa
    table_rowsx = tablex.find_all('tr')
   # un tad tiek lietotas visas rindas iznjemot pirmo (header)
    table_rows = table_rowsx[1:]

   # Taalaak tiek iterets cauri visaam rindaam

    for tr in table_rows:

        id_string = tr.contents[0].contents[0]
        id_text=str(id_string)[10:20]

        location_detailed = tr.contents[3].contents


        data = tr.find_all("td")

        
        ad_text = data[2].get_text()
        majas_stavs = data[4].get_text()
        platiba_m2 = data[5].get_text()
        house_type = data[6].get_text()
        cena = data[7].get_text()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        
        ## print debugging sadaļa
        print("..")
        print(location_detailed)
        print(lpp)
        print(timestamp) 
        
        csv_entry = (id_text, str(location_detailed), str(ad_text), majas_stavs, platiba_m2, house_type, cena, timestamp) 
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?)", csv_entry)
        conn.commit()
        


#main function review
#Veelaak apdomat vai vajadzigi divi while true 

while True:
    while True:
        try:
            for ipasuma_veids in range(2):
                for darijuma_veids in range(2):
                    for lpp in range(lpp_skaits):
                        ss_scraping(lpp, ipasuma_veids, darijuma_veids)
                        time.sleep(1)
            time.sleep(100)
            sys.exit()
        except Exception as e:
            f = open('log.txt', 'w')
            f.write('An exceptional thing happed - %s' % e)
            f.close()
            time.sleep(10)
            pass
    




