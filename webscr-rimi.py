# algoritms
# galvenās sadaļas salistētas ir sarakstā
# linku_saraksts = ("aa", ..)
# 1. kods atver katru linku pēc kārtas,
# 2. piefiksē lapu skaitu apakšā - pagination sarakstā atrodot pēdējo ierakstu
# 3. Tad loopo cauri astoņdesmit produktiem saglabājot to characteristicus datubāzē
# 4. tad iet nākošajā lapā... vai nu uzspiežot next vai nomainot linku...

linku_saraksts = ('https://www.rimi.lv/e-veikals/lv/produkti/augli-un-darzeni/c/SH-2?page=1&pageSize=80&query=', 
                  'https://www.rimi.lv/e-veikals/lv/produkti/gala-zivis-un-gatava-kulinarija/c/SH-6?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/piena-produkti-un-olas/c/SH-11?page=1&pageSize=80&query=',
                  'https://www.rimi.lv/e-veikals/lv/produkti/maize-un-konditoreja/c/SH-7?page=1&pageSize=80&query=',
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

def sadalas_saglabasana(links):
  #apskatas 2.punktu
  for i in range(lapu skaits):
    lapas_saglabasana(links_ar_i)
    
def lapas_saglabasana(links_ar_i)
  #dabuut produktu saraksta kopējo result set supposedly 80 garu
  for i in range(80):
    #save data in database: id, links, timestamp, new price, price type(gab/kg), old price, price in kg, category!)
  
  
  
for links in linku_saraksts:
  try:
    #access link to see if site is not down, if site down, except e thingy logs it and somehow should pass time and try again
    sadalas_saglabasana(links)
