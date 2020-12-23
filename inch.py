

import time
from bs4 import BeautifulSoup
import sys
import sqlite3
import requests
import traceback

conn = sqlite3.connect('result01inch.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()

link_list = ('https://inch.lv/browse?type=apartment&districts=R%C4%ABga&subdistricts=Centrs%2CP%C4%81rdaugava%2C%C4%80genskalns%2CBeberbe%C4%B7i+%28mukupurvs%29%2CBieri%C5%86i-Atg%C4%81zene%2CBi%C5%A1umui%C5%BEa%2CBer%C4%A3i%2CBolder%C4%81ja%2CBukulti%2CBu%C4%BC%C4%BCi%2C%C4%8Ciekurkalns%2CD%C4%81rzciems%2CDaugavgr%C4%ABva%2CDreili%C5%86i%2CDzirciems%2CI%C4%BC%C4%A3uciems%2CImanta%2CJaunciems%2CJugla%2CKatlakalns%2C%C4%B6engarags%2C%C4%B6%C4%ABpsala%2CKleisti%2CKl%C4%ABversala%2CKrasta+rajons%2CManga%C4%BCi+%28m%C4%ABlgr%C4%81vis%29%2CManga%C4%BCsala%2CMaskavas+priek%C5%A1pils.%2CMe%C5%BEaparks%2CMe%C5%BEciems%2CP%C4%BCavnieki%2CPurvciems%2CRumbula%2C%C5%A0amp%C4%93teris-Pleskod%C4%81le%2CSarkandaugava%2C%C5%A0%C4%B7irotava%2CSpilve%2CSu%C5%BEi%2CTeika+%28VEF%29%2CTor%C5%86akalns%2CTr%C4%ABsciems%2CVec%C4%81%C4%B7i%2CVecdaugava%2CVecmilgr%C4%81vis%2CVecr%C4%ABga%2CVoleri%2CZa%C4%B7usala-Lucavsala%2CZasulauks%2CZiepniekkalns%2CZolit%C5%ABde', 
'https://inch.lv/browse?type=apartment&districts=J%C5%ABrmala&subdistricts=Asari%2CBulduri%2CBu%C4%BC%C4%BCuciems%2CBa%C5%BEuciems%2CBra%C5%BEciems%2CDruvciems%2CDubulti%2CDzintari%2CJaundubulti%2CJaun%C4%B7emeri%2CKauguri%2CKaugurciems%2CKrastciems%2CK%C5%ABdra%2C%C4%B6emeri%2CLielupe%2CMajori%2CMellu%C5%BEi%2CPriedaine%2CPumpuri%2CSloka%2CStirnurags%2CVaivari%2CValteri%2CV%C4%81rnukrogs',
'https://inch.lv/browse?type=apartment&districts=R%C4%ABgas+rajons&subdistricts=%C4%80da%C5%BEu+nov.%2CBab%C4%ABtes+pag.%2CBaldones+nov.%2CBalo%C5%BEi%2CCarnikavas+nov.%2CDaugmales+pag.%2CGarkalnes+nov.%2CIn%C4%8Dukalna+nov.%2C%C4%B6ekavas+nov.%2CM%C4%81rupes+pag.%2COlaines+nov.%2CRopa%C5%BEu+nov.%2CSalas+pag.%2CSalaspils+nov.%2CSaulkrasti%2CS%C4%93jas+nov.%2CSiguldas+nov.%2CStopi%C5%86u+nov.',
'https://inch.lv/browse?type=apartment&districts=Aizkraukle+un+raj.',
'https://inch.lv/browse?type=apartment&districts=Al%C5%ABksne+un+raj.'
https://inch.lv/browse?type=house&districts=Balvi+un+raj.
https://inch.lv/browse?type=house&districts=Bauska+un+raj.
https://inch.lv/browse?type=house&districts=C%C4%93sis+un+raj.
https://inch.lv/browse?type=house&districts=Daugavpils+un+raj.











def glabat_slud(link, type):
    r = requests.get(link)
    time.sleep(4)

    soup = BeautifulSoup(r.content, 'html.parser')

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
        sql_entry = (str(ad_id), str(apraksts), str(stavi), str(adrese), str(platiba), "land?", str(cena), str(cena_m2), str(ad_link), "c24", estate_type, str(istabas), stamp) 
        ## db file structure: INTEGER PRIMARY KEY, ad_id, apraksts, stavs, adrese, premise_m2, land_m2, cena, cena_m2, ad_link, ad_source, estate_type, istabas, timestamp
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()
        print(sql_entry)

link = 0
while link != 2:
    try:
        r = requests.get(link_list[link])
        soup = BeautifulSoup(r.content, 'html.parser')
        time.sleep(4)
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
