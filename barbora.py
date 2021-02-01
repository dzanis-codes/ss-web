from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
import requests




#driver.get("https://www.barbora.lv/piena-produkti-un-olas/?order=SortByPopularity&page=20")

#soup = BeautifulSoup(driver.page_source, 'html.parser')

#g_data = soup.find("ul", {"class": "pagination"})




def skaita_lapas(pagination):

    lapu_skaits =[]
    h_data = pagination.find_all("li")
    for hh in h_data:
        k_data = hh.find("a").text

        try:
            m_data = int(k_data)
        except Exception as e:
            m_data = 0
            
        lapu_skaits.append(m_data)
    return max(lapu_skaits)


def savaksana(url):
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    g_data = soup.find("ul", {"class": "pagination"})
    max_lapa = skaita_lapas(g_data)
    
    
    item_data = soup.find_all("div", {"class": "b-product--wrap2 b-product--desktop-grid"})
    
    for item in item_data:
        produkta_isiedati = item.find("div")['data-b-units']
        produkta_pilniedati = item.find("div")['data-b-for-cart']
        pdati = json.loads(produkta_pilniedati)

        prod_id = pdati.get("id")
        prod_nosaukums = pdati.get("title")
        prod_cena = pdati.get("price")
        prod_kategorija = pdati.get("category_name_full_path")
        #print(produkta_pilniedati)
        prod_nr = pdati.get("product_position_in_list")
        print(prod_nr)
        print(prod_nosaukums, "..", prod_cena)
    return max_lapa
    


i = 1
print(i)



while i < 30: #linka_nr < len(linku_saraksts):
    

    try:
        driver = webdriver.Firefox()

        driver.get("https://www.barbora.lv")
        time.sleep(5)

        driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[1]/div/button').click()

        time.sleep(5)
        url = "https://www.barbora.lv/piena-produkti-un-olas/?order=SortByPopularity&page=1"
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        g_data = soup.find("ul", {"class": "pagination"})
        #lielāka pauze pirms katras lielās veikala sadaļas

        lapa = 1

        max_lapa = skaita_lapas(g_data)
        print(max_lapa)

        ##
        ##main funkcija 
        while lapa <= max_lapa:
            i += 1
            print(i)            
            url_part = "page=" + str(lapa)
            full_url = "https://www.barbora.lv/piena-produkti-un-olas/?order=SortByPopularity&page=1" ##linku_saraksts[linka_nr]
            new_url = full_url.replace('page=1', url_part)
            print(url_part)
            ##main funkcija

            max_lapa = savaksana(new_url)

            lapa += 1
        driver.quit()




    
    #šeit pie jebkuras kļūdas augstākesošajā 'try' sadaļā kļūda tiek ielogota ar timestamp un paņemta 10 sekunžu pauze
    #šo sadaļu var saīsināt
    except Exception as e:
        print("e...........")
        time.sleep(5)
        print('\n %s \n' % e)
        pass
# https://www.barbora.lv/augli-un-darzeni?order=SortByPopularity&page=1

#https://stackoverflow.com/questions/60319045/mozilla-firefox-68-2-0esr-browser-is-crashing-using-geckodriver-and-selenium
