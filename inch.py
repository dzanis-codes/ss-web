
import time
from bs4 import BeautifulSoup
import sys
import sqlite3
import requests
import traceback

from selenium import webdriver



options = webdriver.ChromeOptions()
#options.add_argument('--window-size=800,400')  
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

conn = sqlite3.connect('result01inch.db') ## jaapapildina datubaze ar kolonnām; nosaukt jaunu datubazes failu
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, ad_link, stavi_kopa, adrese, platiba, land, cena, cena_m2, source, transaction_type, estate_type, istabas, stamp)''')
# Save (commit) the changes
conn.commit()


link_list = ('https://inch.lv/browse?type=apartment&districts=R%C4%ABga&subdistricts=Centrs%2CP%C4%81rdaugava%2C%C4%80genskalns%2CBeberbe%C4%B7i+%28mukupurvs%29%2CBieri%C5%86i-Atg%C4%81zene%2CBi%C5%A1umui%C5%BEa%2CBer%C4%A3i%2CBolder%C4%81ja%2CBukulti%2CBu%C4%BC%C4%BCi%2C%C4%8Ciekurkalns%2CD%C4%81rzciems%2CDaugavgr%C4%ABva%2CDreili%C5%86i%2CDzirciems%2CI%C4%BC%C4%A3uciems%2CImanta%2CJaunciems%2CJugla%2CKatlakalns%2C%C4%B6engarags%2C%C4%B6%C4%ABpsala%2CKleisti%2CKl%C4%ABversala%2CKrasta+rajons%2CManga%C4%BCi+%28m%C4%ABlgr%C4%81vis%29%2CManga%C4%BCsala%2CMaskavas+priek%C5%A1pils.%2CMe%C5%BEaparks%2CMe%C5%BEciems%2CP%C4%BCavnieki%2CPurvciems%2CRumbula%2C%C5%A0amp%C4%93teris-Pleskod%C4%81le%2CSarkandaugava%2C%C5%A0%C4%B7irotava%2CSpilve%2CSu%C5%BEi%2CTeika+%28VEF%29%2CTor%C5%86akalns%2CTr%C4%ABsciems%2CVec%C4%81%C4%B7i%2CVecdaugava%2CVecmilgr%C4%81vis%2CVecr%C4%ABga%2CVoleri%2CZa%C4%B7usala-Lucavsala%2CZasulauks%2CZiepniekkalns%2CZolit%C5%ABde', 
'https://inch.lv/browse?type=apartment&districts=J%C5%ABrmala&subdistricts=Asari%2CBulduri%2CBu%C4%BC%C4%BCuciems%2CBa%C5%BEuciems%2CBra%C5%BEciems%2CDruvciems%2CDubulti%2CDzintari%2CJaundubulti%2CJaun%C4%B7emeri%2CKauguri%2CKaugurciems%2CKrastciems%2CK%C5%ABdra%2C%C4%B6emeri%2CLielupe%2CMajori%2CMellu%C5%BEi%2CPriedaine%2CPumpuri%2CSloka%2CStirnurags%2CVaivari%2CValteri%2CV%C4%81rnukrogs',
'https://inch.lv/browse?type=apartment&districts=R%C4%ABgas+rajons&subdistricts=%C4%80da%C5%BEu+nov.%2CBab%C4%ABtes+pag.%2CBaldones+nov.%2CBalo%C5%BEi%2CCarnikavas+nov.%2CDaugmales+pag.%2CGarkalnes+nov.%2CIn%C4%8Dukalna+nov.%2C%C4%B6ekavas+nov.%2CM%C4%81rupes+pag.%2COlaines+nov.%2CRopa%C5%BEu+nov.%2CSalas+pag.%2CSalaspils+nov.%2CSaulkrasti%2CS%C4%93jas+nov.%2CSiguldas+nov.%2CStopi%C5%86u+nov.',
'https://inch.lv/browse?type=apartment&districts=Aizkraukle+un+raj.',
'https://inch.lv/browse?type=apartment&districts=Al%C5%ABksne+un+raj.',
'https://inch.lv/browse?type=house&districts=Balvi+un+raj.',
'https://inch.lv/browse?type=house&districts=Bauska+un+raj.',
'https://inch.lv/browse?type=house&districts=C%C4%93sis+un+raj.',
'https://inch.lv/browse?type=house&districts=Daugavpils+un+raj.')











def glabat_slud(link, type):
    print(link)
    driver = webdriver.Chrome('chromedriver',options=options)
    print("..x")
 
    driver.get(link)
    time.sleep(4)
    #r = requests.get(link)
    #time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #print(soup)
    g_data = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['browse-card-wrapper'])

    print(len(g_data))

#    h_data = soup.find_all("div", {"class": "browse-card-wrapper"})
    #print(h_data)
    #print(g_data)

#vajag range pareizi saskaitīt
    for count in range(120):
        print("count:", count)
        print(g_data[count])
        #ad_id = g_data[count].find("data-object-id")
        #print(ad_id)



        ad_link = g_data[count].find("a")['href']
        print(ad_link)
        #img_link = h_data[count].find("img")['src']
        
        adrese_tag = g_data[count].find("div", {"class": "browse-card__address__text"})
        #print(adrese_tag)
        adrese = adrese_tag.text
        print(adrese)
        


        cena_tag = g_data[count].find("div", {"class": "browse-card__cost__price"})
        #print(cena_tag)
        cena = cena_tag.text
        print(cena)
        rent_tag = g_data[count].find("div", {"class": "browse-card__cost__rent-per"})
        if rent_tag != None:
          transaction = rent_tag.text
          print(transaction)
        else:
          transaction = "Sale"


        cena_m2_tag = g_data[count].find("div", {"class": "browse-card__cost__per-area"})
        cena_m2 = cena_m2_tag.text
        print(cena_m2)

        citsinfo = g_data[count].find("div", {"class": "browse-card__middle"})
        desc_list = citsinfo.find_all("div", {"class": "browse-card__item"}) 
        #print(len(desc_list))
        for a in range(len(desc_list)):
            #print(desc_list[a])
            print(desc_list[a].text)
        istabas = desc_list[0].text
        #istabas = citsinfo.find("i", {"class": "icon-bedroom"})
        #print(istabas)
        stavs = desc_list[1].text
        stavi_kopa = stavs

        #stavs = citsinfo.find("i", {"class": "icon-staircase"})
        #print(stavs)
        platiba = istabas = desc_list[2].text




        


        ts = time.gmtime()
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)

        sql_entry = (str(ad_link), str(stavi_kopa), str(adrese), str(platiba), "land?", str(cena), str(cena_m2), "inch.lv", str(transaction), "appartment", str(istabas), stamp) 
        print(sql_entry)

        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
        
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
