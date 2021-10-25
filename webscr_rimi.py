# -*- coding: utf-8 -*-
##Papildināt ar funkciju, kas pie None type atrašanas dod False vai "na"


#No importiem sys vajadzīgs tikai tādēļ lai beigās aizvērtu failu, un re vajadzīgs tikai vienā vietā, ko var pārtaisīt savādāk
import time
from bs4 import BeautifulSoup
import sys
import requests
import sqlite3
import re
import traceback

#Tiek izveidots pieslēgums datubāzei, kur savāktie dati tiks glabāti. datubāzes izveide ir atsevišķs skripts šajā folderī
#Var pamainīt: (1) iekļaut datubāzes veidošanu šajā skriptā (if does not exist); (2) var taisīt katru nedēļu jaunu datubāzi 
path = '/LBData/Retail/result01rimi.db'

conn = sqlite3.connect(path) 
c = conn.cursor()

#Šī ir galvenā funkcija, kas lieto "links" kā input, linku kurā ieiet un savākt un saglabāt datus no šī linka
def savaksana(links):
    
    #tiek atvērts links
    r = requests.get(links)
    
    #Pauze 1 sekunde, lai neapgrūtinātu serveri un varētu mierīgi ielādēt linku
    time.sleep(1)
    
    #lapas saturs tiek padarīts "saprotams"
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #tiek atrasta sadaļa ar produktiem
    p_data = soup.find("ul", {"class": "product-grid"})
    
    #tiek atrasts produktu saraksts
    item_data = p_data.find_all("li", {"class": "product-grid__item"})
    
    #tālāk seko loop atrastajam produktu sarakstam, kur tiek iziets cauri katram produkta "lodziņam"
    for item in item_data:
        
        #Tiek saglabats produkta id, nosaukums, un links
        produkta_id = item.find("div")['data-product-code']
        prod_nosaukums = item.find("div")['data-gtms-click-name']
        prod_links = item.find("a")['href']
        
        #šeit quick-and-dirty veidā tiek pārbaudīts vai produkta nosaukums nav tukšs
        if type(item.find("p", {"class": "card__name"})) == type(item.find("p", {"class": "tests nav miris"})):
            prod_nosaukums2 = "na"        
        else:
            prod_nosaukums2 = item.find("p", {"class": "card__name"}).text
            
        #tiek atrasti iekšējie dati un cenas lauciņš    
        prod_internal_data = item.find("div")['data-gtm-eec-product']
        cena_tag = item.find("div", {"class": "card__price"})
        cenas_komp=[]
        
        #šeit quick-and-dirty veidā tiek pārbaudīts vai cenas lauciņš nav tukšs, jo daži produkti nav pieejami
        if type(cena_tag) == type(item.find("p", {"class": "tests nav miris"})):
            print("nav pieejams")
            cena = "na"
            pilna_cena = "na"
            discount = "na"
            cena_pirms_atl = "na"
        else:
            for x in cena_tag:
                cenas_komp.extend(x)
                
            #šeit tālāk tiek salikta cena (jo eirocenti ir attēloti atšķirīgi)
            cena = str(cenas_komp[1]) +"." + str(cenas_komp[4].text)
            
            #šī sadaļa ir par gab./kg
            cena_parko = cenas_komp[6].text
            
            #šeit quick-and-dirty veidā tiek pārbaudīts vai ir pilnā cena (atšķirībā no iepakojuma cenas)
            if type(item.find("p", {"class": "card__price-per"})) == type(item.find("p", {"class": "tests nav miris"})):
                pilna_cena = "na"
            else:
                pilna_cena_tag = item.find("p", {"class": "card__price-per"}).text
                pilna_cena = re.sub(r"[\n\t\s]*", "", pilna_cena_tag) 
                
            #šeit quick-and-dirty veidā tiek pārbaudīts vai ir atlaide
            if type(item.find("div", {"class": "old-price-tag card__old-price"})) != type(item.find("p", {"class": "tests nav miris"})):
                old_price_tag = item.find("div", {"class": "old-price-tag card__old-price"}).text
                discount = "yes"
                cena_pirms_atl = re.sub(r"[\n\t\s]*", "", old_price_tag)
            else:
                cena_pirms_atl = "na"
                discount="no"
        
        avots = "rimi"
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        
        #šeit tiek apkopoti visi savāktie dati, tiek "izprintēti" bugfixing nolūkiem un tad tiek ievietoti datubāzē
        sql_entry = (str(produkta_id), str(prod_nosaukums), str(prod_links), str(prod_nosaukums2), str(prod_internal_data), str(cena), str(pilna_cena), str(discount), str(cena_pirms_atl), str(avots), timestamp)
        print(sql_entry)
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        conn.commit()



#internetveikala sadaļu linku saraksts  
linku_saraksts = ('https://www.rimi.lv/e-veikals/lv/produkti/augli-un-darzeni/c/SH-2?page=1&pageSize=80&query=', 
                  'https://www.rimi.lv/e-veikals/lv/produkti/gala-zivis-un-gatava-kulinarija/c/SH-6?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/maize-un-konditoreja/c/SH-7?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/piena-produkti-un-olas/c/SH-11?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/saldetie-edieni/c/SH-12?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/iepakota-partika/c/SH-4?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/saldumi-un-uzkodas/c/SH-13?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/dzerieni/c/SH-5?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/alkoholiskie-dzerieni/c/SH-1?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/zidainiem-un-berniem/c/SH-15?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/skaistumkopsanai-un-higienai/c/SH-14?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/sadzives-kimija/c/SH-10?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/majdzivniekiem/c/SH-8?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/majai-darzam-un-atputai/c/SH-3?page=1&pageSize=80&query=')

#atskaites mainīgais
linka_nr = 0

#_main_ skripta daļa, kas ir loop izejot cauri katram linkam
while linka_nr < len(linku_saraksts):
    
    #try...except nozīmē, ka funkcija tiek pildīta līdz error un pēc tam tiek turpināta
    try:
        r = requests.get(linku_saraksts[linka_nr])
        
        #lielāka pauze pirms katras lielās veikala sadaļas
        time.sleep(5)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        #tiek atrasta lapu numuru sadaļa un iegūts kopējais lapu skaits veikala sadaļā
        g_data = soup.find("div", {"class": "pagination"})
        h_data = g_data.find_all("li", {"class": "pagination__item"})
        lapu_skaits = int(h_data[-2].text) + 1

        #šajā loop tiek iziets cauri katrai lapai interneta veikala sadaļā un tiek saglabāts katras lapas saturs
        for lapa in range(1, lapu_skaits):
            url_part = "page=" + str(lapa)
            full_url = linku_saraksts[linka_nr]
            new_url = full_url.replace('page=1', url_part)
            print(url_part)
            savaksana(new_url)
        linka_nr += 1
    
    #šeit pie jebkuras kļūdas augstākesošajā 'try' sadaļā kļūda tiek ielogota ar timestamp un paņemta 10 sekunžu pauze
    #šo sadaļu var saīsināt
    except Exception as e:
        error_path = '/LBApp_log/errorlog_rimi.txt'
        f = open(error_path, 'a+')
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        f.write('\n %s \n' % e)
        tb = traceback.TracebackException.from_exception(e)
        f.write('\n'.join(tb.stack.format()))            
        f.write('\n %s \n' % timestamp)
        f.close()
        time.sleep(10)
        pass        

#kad viss pabeigts, tad skripta fails tiek aizvērts    
sys.exit()
