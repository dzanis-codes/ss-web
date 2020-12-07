


import time
from bs4 import BeautifulSoup
import sys
import requests
import sqlite3
import re

conn = sqlite3.connect('result01rimi.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()

def savaksana(links):
    r = requests.get(links, verify = False)
    time.sleep(4)
    soup = BeautifulSoup(r.content, 'html.parser')

    p_data = soup.find("ul", {"class": "product-grid"})
    item_data = p_data.find_all("li", {"class": "product-grid__item"})
    for item in item_data[0:12]:

        print("...")
        #1.dati
        produkta_id = item.find("div")['data-product-code']
        prod_nosaukums = item.find("div")['data-gtms-click-name']
        prod_links = item.find("a")['href']
        prod_nosaukums2 = item.find("p", {"class": "card__name"}).text
        prod_internal_data = item.find("div")['data-gtm-eec-product']
        cena_tag = item.find("div", {"class": "card__price"})
        cenas_komp=[]
        if type(cena_tag) == type(item.find("p", {"class": "tests nav miris"})):
            print("nav pieejams")
            cena = "na"
            pilna_cena = "na"
            discount = "na"
            cena_pirms_atl = "na"
        else:

            for x in cena_tag:
                cenas_komp.extend(x)

            cena = str(cenas_komp[1]) +"." + str(cenas_komp[4].text)
            cena_parko = cenas_komp[6].text

            pilna_cena_tag = item.find("p", {"class": "card__price-per"}).text
            pilna_cena = re.sub(r"[\n\t\s]*", "", pilna_cena_tag)

            if type(item.find("p", {"class": "card__old-price"})) != type(item.find("p", {"class": "tests nav miris"})):
                old_price_tag = item.find("p", {"class": "card__old-price"}).text

                cena_pirms_atl = re.sub(r"[\n\t\s]*", "", old_price_tag)
            else:
                cena_pirms_atl = "na"
                discount="no"
        avots = "rimi"
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))
        sql_entry = (str(produkta_id), str(prod_nosaukums), str(prod_links), str(prod_nosaukums2), str(prod_internal_data), str(cena), str(pilna_cena), str(discount), str(cena_pirms_atl), str(avots), timestamp)
        print(sql_entry)
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        conn.commit()



  
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

linka_nr = 0
while linka_nr < len(linku_saraksts):
    try:
        r = requests.get(linku_saraksts[linka_nr], verify = False)
        time.sleep(5)
        soup = BeautifulSoup(r.content, 'html.parser')

        g_data = soup.find("div", {"class": "pagination"})
        h_data = g_data.find_all("li", {"class": "pagination__item"})
        lapu_skaits = int(h_data[-2].text) + 1

        for lapa in range(1, lapu_skaits):
            url_part = "page=" + str(lapa)
            full_url = linku_saraksts[linka_nr]
            new_url = full_url.replace('page=1', url_part)
            print(url_part)
            savaksana(new_url)

        linka_nr += 1
    except Exception as e:
        f = open('log_rimi.txt', 'a+')
        ts = time.gmtime()
        timestamp = (time.strftime("%Y-%m-%d %H:%M:%S", ts))

        f.write('\n %s \n' % e)
        f.write('\n %s \n' % timestamp)
        f.write('\n error atverot linku nr.: '.join(str(linka_nr)))
        f.close()
        time.sleep(10)
        pass        

sys.exit()
