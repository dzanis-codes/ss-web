import requests
import time
from bs4 import BeautifulSoup

ts = time.gmtime()

saraksts_darij = ["sell", "hand_over"]
saraksts_veids = ["flats", "homes-summer-residences", "farms-estates", "premises", "offices"]
        

url = "https://www.ss.com/lv/real-estate/farms-estates/today/hand_over/"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
print("1")
## tiek atlasitas visas tabulas
tables = soup.findAll('table')
print("2")
print(len(tables))

#tiek ieguts sludinajumu skaits
slud_skaits = tables[1].find_all("option")[2].get_text()
skaits_n = slud_skaits.split()[-1]
print("3")

#lpp skaits ir ar uzviju, un tad ir dublikati
lpp_skaits = round(int(skaits_n) / 30) + 4
print("4")

## tad jaabuut funkcijai kas iteree cauri visaam lapaam
## shai funkcijai divi papildinajumi:
## 1. papildinajums ir mainigais vai sell/handover - maina tikai adresi
## 2. papildinajums ir mainigais par ni tipu - mainas adrese, kolonnas atzimejama informacija
def ss_scraping(lpp, ipasuma_veids, darijuma_veids):
    url = "https://www.ss.com/lv/real-estate/" + str(saraksts_veids[ipasuma_veids]) + "/today/" + str(saraksts_darij[darijuma_veids]) + "/page"+ str(lpp)+".htmll"
    print(url)
    
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
        ad_text = data[2].get_text()
        linky = data[1].find('a')['href']
        location_detailed = tr.contents[3].contents ## vai var uzlavot ar data.get_text?
        if ipasuma_veids == 0:
                ##flats
                platiba_m2 = data[5].get_text()
                majas_stavs = data[4].get_text()
                house_type = data[6].get_text()
                cena = data[7].get_text()
                ##taalaak vajadzees elifus
        else:
                ##house
                platiba_m2 = data[4].get_text()
                majas_stavs = data[5].get_text()
                house_type = "na"
                room_count = data[6].get_text()
                land_m2 = data[7].get_text()
                cena = data[8].get_text()
   
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        print(linky)
        ## print debugging sadaļa
        print("..")
        print("flat = 0, maja = 1")
        print(ipasuma_veids)
        print("..")
        print(location_detailed)
        print(lpp)
        print(timestamp) 
        
        


#main function review
#Veelaak apdomat vai vajadzigi divi while true 

while True:
    while True:
        try:
            for ipasuma_veids in range(1,3):
                for darijuma_veids in range(2):
                    for lpp in range(lpp_skaits):
                        
                                                ##šeit laikam ielikt error handling
                        url = "https://www.ss.com/lv/real-estate/" + str(saraksts_veids[ipasuma_veids]) + "/today-2/" + str(saraksts_darij[darijuma_veids]) + "/page"+ str(lpp)+".html"
                        ##papildus error handling šeit laikam vajag vai requests nostrādā, vai ko darit ja lapa ir down
                        r = requests.get(url)
                        soup = BeautifulSoup(r.content, 'html.parser')
                        tables = soup.findAll('table')
                        tablex = tables[4]
                        print(url)
                        print("ecc")                 
                        if "sludinājumi nav atrasti" in tablex.get_text():
                                print("check")
                                ## vajadzētu ielogot šo gadījumu
                                break
                        
                        ss_scraping(lpp, ipasuma_veids, darijuma_veids)
                        time.sleep(1)
            time.sleep(100)
            break
        except Exception as e:
            f = open('log.txt', 'w')
            f.write('An exceptional thing happed - %s' % e)
            f.close()
            time.sleep(10)
            pass
    

