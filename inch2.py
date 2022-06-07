import requests
import time
import sys
import sqlite3
import traceback

conn = sqlite3.connect('result01inch.db') 
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, id, city, district, address, longitude, latitude, userUpdatedAt, dealType, rentPriceUnit, area, roomCount, floorNumber, floorTotal, price, type, stamp)''')


conn.commit()

link_list = ('https://api.inch.lv/api/search/apartments?city=R%C4%ABga&subdistricts=Centrs%2CP%C4%81rdaugava%2C%C4%80genskalns%2CBeberbe%C4%B7i+%28mukupurvs%29%2CBieri%C5%86i-Atg%C4%81zene%2CBi%C5%A1umui%C5%BEa%2CBer%C4%A3i%2CBolder%C4%81ja%2CBukulti%2CBu%C4%BC%C4%BCi%2C%C4%8Ciekurkalns%2CD%C4%81rzciems%2CDaugavgr%C4%ABva%2CDreili%C5%86i%2CDzirciems%2CI%C4%BC%C4%A3uciems%2CImanta%2CJaunciems%2CJugla%2CKatlakalns%2C%C4%B6engarags%2C%C4%B6%C4%ABpsala%2CKleisti%2CKl%C4%ABversala%2CKrasta+rajons%2CManga%C4%BCi+%28m%C4%ABlgr%C4%81vis%29%2CManga%C4%BCsala%2CMaskavas+priek%C5%A1pils.%2CMe%C5%BEaparks%2CMe%C5%BEciems%2CP%C4%BCavnieki%2CPurvciems%2CRumbula%2C%C5%A0amp%C4%93teris-Pleskod%C4%81le%2CSarkandaugava%2C%C5%A0%C4%B7irotava%2CSpilve%2CSu%C5%BEi%2CTeika+%28VEF%29%2CTor%C5%86akalns%2CTr%C4%ABsciems%2CVec%C4%81%C4%B7i%2CVecdaugava%2CVecmilgr%C4%81vis%2CVecr%C4%ABga%2CVoleri%2CZa%C4%B7usala-Lucavsala%2CZasulauks%2CZiepniekkalns%2CZolit%C5%ABde&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121', 
'https://api.inch.lv/api/search/apartments?city=J%C5%ABrmala&subdistricts=Asari%2CBulduri%2CBu%C4%BC%C4%BCuciems%2CBa%C5%BEuciems%2CBra%C5%BEciems%2CDruvciems%2CDubulti%2CDzintari%2CJaundubulti%2CJaun%C4%B7emeri%2CKauguri%2CKaugurciems%2CKrastciems%2CK%C5%ABdra%2C%C4%B6emeri%2CLielupe%2CMajori%2CMellu%C5%BEi%2CPriedaine%2CPumpuri%2CSloka%2CStirnurags%2CVaivari%2CValteri%2CV%C4%81rnukrogs&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=R%C4%ABgas+rajons&subdistricts=%C4%80da%C5%BEu+nov.%2CBab%C4%ABtes+pag.%2CBaldones+nov.%2CBalo%C5%BEi%2CCarnikavas+nov.%2CDaugmales+pag.%2CGarkalnes+nov.%2CIn%C4%8Dukalna+nov.%2C%C4%B6ekavas+nov.%2CM%C4%81rupes+pag.%2COlaines+nov.%2CRopa%C5%BEu+nov.%2CSalas+pag.%2CSalaspils+nov.%2CSaulkrasti%2CS%C4%93jas+nov.%2CSiguldas+nov.%2CStopi%C5%86u+nov.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Aizkraukle+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Al%C5%ABksne+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Balvi+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Bauska+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=C%C4%93sis+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Daugavpils+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Dobele+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Gulbene+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=J%C4%93kabpils+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Jelgava+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Kr%C4%81slava+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Kuld%C4%ABga+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Liep%C4%81ja+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Limba%C5%BEi+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Ludza+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Madona+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Ogre+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Prei%C4%BCi+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=R%C4%93zekne+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Saldus+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Talsi+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Tukums+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Valka+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Valmiera+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121',
'https://api.inch.lv/api/search/apartments?city=Ventspils+un+raj.&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121')


type_list = ('apartments?', 'houses?', 'lands?', 'commercials?commercialType=office&', 'commercials?commercialType=trade&', 'commercials?commercialType=industrial&')


def glabat_slud(ad_json, type):
  id = ad_json[0]
  city = ad_json[1]
  district = ad_json[2]
  address = ad_json[3]
  longitude = ad_json[4]
  latitude = ad_json[5]
  userUpdatedAt = ad_json[6]
  dealType = ad_json[7]
  rentPriceUnit = ad_json[8]
  area = ad_json[9]
  roomCount = ad_json[10]
  floorNumber = ad_json[11]
  floorTotal = ad_json[12]
  price = ad_json[13]
  
  ts = time.gmtime()
  stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
  sql_entry = (str(id), str(city), str(district), str(address), str(longitude), str(latitude), str(userUpdatedAt), str(dealType), str(rentPriceUnit), str(area), str(roomCount), str(floorNumber), str(floorTotal), str(price), str(type), stamp) 
  #print(sql_entry)
  c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
  conn.commit()
  #time.sleep(1)


for category in type_list:
  print(category)
  for each_link in link_list:
    if category == 'apartments?':
      modified_link = each_link[:31] + category + each_link[42:]
    elif category == 'houses?'
      modified_link = each_link[:31] + category + each_link[42:-30] + '&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,houseArea,roomCount,landArea&offset=0&limit=121'
    print(modified_link)
    r = requests.get(modified_link)
    print(r.json())
    section = category[:-1]
    for ad_json in r.json()[section]['data']:
      glabat_slud(ad_json, category)
    time.sleep(3)
#  dataset = (id, city, district, address, longitude, latitude, userUpdatedAt, dealType, rentPriceUnit, area, roomCount, floorNumber, floorTotal, price)
# vajag pārbaudīt kas notiek ar tukšajiem ierakstiem


