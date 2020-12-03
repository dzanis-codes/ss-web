## pedejas izmaiņas:
## 1. izņēmu csv rakstīšanu ārā
## 2. pamainīšu datubāzi un šo jāpalaiž kā papildu jaunu event paralēli vecajam... ja nu kaut kas nobrūk

import sys
import requests
import time
from bs4 import BeautifulSoup
import sqlite3



## Datubāzei vairāki papildinājumi: pielikt kolonnu "saite", kolonnu "darijums - ar opciju pardod/izire", kolonnu "avots", kur bus ss.com, kolonnu "nek.veids" 
## ar attieciguiem mainigajiem dzivoklis, maja, zeme, vasarnica, telpas, biroji
## un tad vēl jaunas kolonnas zemes pl. (kur ir m2 vai ha vai na) 
conn = sqlite3.connect('result02.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()
saraksts_darij = ["sell", "hand_over"]
saraksts_veids = ["flats", "homes-summer-residences", "farms-estates", "offices", "plots-and-lands"]
        
## šeit seko lapu izskaitīšana 
## vai to vajag katram veidam? Varētu to izdarīt lai mazāk dublikātu

url = "https://www.ss.com/lv/real-estate/flats/today-2/sell/"
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
def ss_scraping(lpp, ipasuma_veids, darijuma_veids):
    url = "https://www.ss.com/lv/real-estate/" + str(saraksts_veids[ipasuma_veids]) + "/today-2/" + str(saraksts_darij[darijuma_veids]) + "/page"+ str(lpp)+".html"
    
##!! šeit vajag īpašo error handling , ja vispār nav neviena šāda sludinājuma
        
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
        
        ##!! kas notiks kad pieprasisim vairak kolonnas nekaa ir?; varbut nepieprasisim ar pareizu if elif else strukturu
        
        data = tr.find_all("td")
        id_string = tr.contents[0].contents[0] ## vai var uzlavot ar data.get_text?
        id_text=str(id_string)[10:20]
        linky = data[1].find('a')['href']
        ad_text = data[2].get_text()
        location_detailed = tr.contents[3].contents ## vai var uzlavot ar data.get_text?
        

        #galvenā datu sagrupēšanas sadaļa no veidiem
        
        if ipasuma_veids == 0:
                ##flats
                platiba_m2 = data[5].get_text()
                majas_stavs = data[4].get_text()
                house_type = data[6].get_text()
                cena = data[7].get_text()
                land_m2 = "na"
                room_count = "na"
                ##taalaak vajadzees elifus
        elif ipasuma_veids == 1:
                ##house
                platiba_m2 = data[4].get_text()
                majas_stavs = data[5].get_text()
                house_type = "na"
                room_count = data[6].get_text()
                land_m2 = data[7].get_text()
                cena = data[8].get_text()
        elif ipasuma_veids == 2:
                ##viensetas
                platiba_m2 = data[5].get_text()
                majas_stavs = data[4].get_text()
                house_type = "na"
                room_count = "na"
                land_m2 = data[6].get_text()
                cena = data[7].get_text()
        elif ipasuma_veids == 3:
                ##biroji
                platiba_m2 = data[4].get_text()
                majas_stavs = data[5].get_text()
                house_type = "na"
                room_count = "na"
                land_m2 = "na"
                cena = data[6].get_text()
        else:
                ##zeme
                platiba_m2 = data[4].get_text()
                majas_stavs = "na"
                house_type = "na"
                room_count = "na"
                land_m2 = "na"
                cena = data[5].get_text()
                
   
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        
        ## print debugging sadaļa
        print("..")
        print("flat = 0, maja = 1")
        print(ipasuma_veids)
        print(location_detailed)
        print(lpp)
        print(timestamp) 
        
        ## uzreiz iekš entry var ielikt str(saraksts_veids[darijuma_veids])
        ## vel var ielikt uzreiz avotu ss.com
        avots = 'ss.com'
        estate_type = saraksts_veids[ipasuma_veids]
        transaction_type = saraksts_darij[darijuma_veids]
        sql_entry = (id_text, str(ad_text), majas_stavs, str(location_detailed), platiba_m2, land_m2, house_type, cena, linky, avots, estate_type, transaction_type, timestamp) 
        ## db file structure: name_id INTEGER PRIMARY KEY, ad_id, ad_text, stavs, location, premise_m2, land_m2, house_type, cena, ad_link, ad_source, estate_type, transaction_type, timestamp
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()
        


#main function review
#Veelaak apdomat vai vajadzigi divi while true 

while True:
    while True:
        try:
            for ipasuma_veids in range(5):
                for darijuma_veids in range(2):
                    for lpp in range(lpp_skaits):
                        
                        try:
                            ss_scraping(lpp, ipasuma_veids,darijuma_veids)
                        except IndexError:
                            f = open('log_ss.txt', 'a')
                            ts = time.gmtime()
                            timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
                            ## Šeit jāsaformatē error logging
                            liste = (saraksts_darij[darijuma_veids], saraksts_veids[ipasuma_veids], lpp)
                            f.write('\n %s \n' % str(timestamp))
                            f.write('\nIndex error: '.join(str(item) for item in liste))
                            f.close()
                            pass
                        continue

                        time.sleep(1)
            time.sleep(100)
            sys.exit()
        except Exception as e:
            f = open('log_ss.txt', 'a')
            f.write('An exceptional thing happed - %s' % e)
            ts = time.gmtime()
            timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
            f.write('time: %s' % timestamp
            f.close()
            time.sleep(10)
            pass
        continue
    



## tālākai nākotnei - izdarīto darbību skaitu vajag kautkur uzskaitīt un monitorēt onlainā, lai pamanām ja kas apstājies
