import requests
import time
import sys
import sqlite3
import traceback


path = '/LBData/jaunakie_dati/results_inch.db'
conn = sqlite3.connect(path) 
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, id, city, district, address, longitude, latitude, userUpdatedAt, dealType, rentPriceUnit, area, roomCount, floorNumber, floorTotal, price, landArea, type, stamp)''')


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


type_list = {'apartments?' : '&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber,floorTotal&offset=0&limit=121', 'houses?' : '&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,houseArea,roomCount,landArea&offset=0&limit=121', 'lands?':'&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area&offset=0&limit=121', 'commercials?commercialType=office&':'&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,floorNumber,floorTotal&offset=0&limit=121', 'commercials?commercialType=trade&':'&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,floorNumber,floorTotal&offset=0&limit=121', 'commercials?commercialType=industrial&':'&optimize=1&fields=id,images,city,district,address,longitude,latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,floorNumber,floorTotal&offset=0&limit=121'}


def glabat_slud(ad_json, type, category):
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
  #nākošajām vērtībām ir dažāda kārtība un eksistence atkarībā no type
  if (type == 'apartments') or (type == 'houses'):
    roomCount = ad_json[10]
  else:
    roomCount = 'na'    

  if (type == 'lands') or (type == 'houses'):
    floorNumber = 'na'
  elif type == 'apartments':
    floorNumber = ad_json[11]  
  else:
    floorNumber = ad_json[10]   

  if (type == 'lands') or (type == 'houses'):
    floorTotal = 'na'
  elif type == 'apartments':
    floorTotal = ad_json[12]  
  else:
    floorTotal = ad_json[11]   


#{'header': ['id', 'city', 'district', 'address', 'longitude', 'latitude', 'userUpdatedAt', 'dealType', 'rentPriceUnit', 'area', 'floorNumber', 'floorTotal', 'price', 'processingImages', 'images'], 'data': [[13555, 'Preiļi un raj.', None, 'Jaunsilavas 3, ', 26.166, 56.393384, '2022-05-01T16:14:37.351Z', 'sale', None, 710.9, 1, 1, 120000.0, False, {'keys': ['image0.jpg', 'image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg', 'image9.jpg', 'image10.jpg', 'image11.jpg', 'image12.jpg', 'image13.jpg', 'image14.jpg', 'image15.jpg', 'image16.jpg', 'image17.jpg', 'image18.jpg', 'image19.jpg', 'image20.jpg'], 't': 1651453023}], [14412, 'Preiļi un raj.', None, 'Meža iela 19F, Līvāni, Līvānu pilsēta, Latvija', 26.1714054, 56.3457238, '2022-05-01T08:19:55.050Z', 'sale', None, 337.0, 1, 2, 97000.0, False, {'keys': ['image0.jpg', 'image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg', 'image9.jpg', 'image10.jpg', 'image11.jpg', 'image12.jpg', 'image13.jpg', 'image14.jpg', 'image15.jpg', 'image16.jpg', 'image17.jpg', 'image18.jpg', 'image19.jpg', 'image20.jpg', 'image21.jpg', 'image22.jpg'], 't': 1651393195}], [17157, 'Preiļi un raj.', None, 'Baznīcas iela 29, Līvāni, Līvānu pilsēta, Latvia', 26.1641459, 56.3666848, '2022-04-20T09:45:10.568Z', 'sale', None, 3800.0, 2, 2, 350000.0, False, {'keys': ['image0.jpg', 'image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg', 'image9.jpg', 'image10.jpg', 'image11.jpg', 'image12.jpg', 'image13.jpg', 'image14.jpg', 'image15.jpg', 'image16.jpg', 'image17.jpg', 'image18.jpg', 'image19.jpg', 'image20.jpg', 'image21.jpg', 'image22.jpg', 'image23.jpg'], 't': 1650447910}], [13255, 'Preiļi un raj.', None, 'Baznīcas iela 25, Līvāni, Līvānu pilsēta, Latvija', 26.1642779, 56.3667048, '2022-03-29T06:55:10.512Z', 'sale', None, 573.8, 2, 2, 69000.0, False, {'keys': ['image0.jpg', 'image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg', 'image9.jpg', 'image10.jpg', 'image11.jpg', 'image12.jpg', 'image13.jpg'], 't': 1648536910}]], 'meta': {'images': {'prefix': 'https://i.inch.lv/images/commercial/', 'placeholders': {'view': 'https://i.inch.lv/images/placeholder/view_placeholder.jpg', 'preview': 'https://i.inch.lv/images/placeholder/preview_placeholder.jpg', 'full': 'https://i.inch.lv/images/placeholder/full_placeholder.jpg'}}}}}

  if type == 'lands':
    price = ad_json[10]
  elif type == 'apartments':
    price = ad_json[13]
  else:
    price = ad_json[12]

  if type == 'houses':
    landArea = ad_json[11]
  else:
    landArea = "na"
  typex = category

  ts = time.gmtime()
  stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
  sql_entry = (str(id), str(city), str(district), str(address), str(longitude), str(latitude), str(userUpdatedAt), str(dealType), str(rentPriceUnit), str(area), str(roomCount), str(floorNumber), str(floorTotal), str(price), str(landArea), str(typex), stamp) 
  #print(sql_entry)
  c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sql_entry)
  conn.commit()
  #time.sleep(1)



type_nr = 0
while type_nr < len(type_list):    
  print("While " + str(type_nr) + " is less than " + str(len(type_list)))
  for category in type_list:
    print(category)
    for each_link in link_list:
      try:
        modified_link = each_link[:31] + category + each_link[42:-169] + type_list[category]
        print(modified_link)
        r = requests.get(modified_link)
        print(r.json())    
        section = category[:-1]
        if section[:11] == "commercials":
          section = "commercials"
        for ad_json in r.json()[section]['data']:
          glabat_slud(ad_json, section, category)
        time.sleep(3)
        type_nr = type_nr + 1
      except Exception as e:
        error_path = '/LBApp_log/errorlog_inch.txt'
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
   
sys.exit()







