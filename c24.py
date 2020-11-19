from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get('https://www.city24.lv/lv/saraksts?fr=0&lang=lv&usp=true&ord=sort-date-desc')

select = Select(driver.find_element_by_id('new-search__column new-search__column--w20 new-search__transaction-type'))


print select.options
print [o.text for o in select.options] # these are string-s

## select by visible text
#select.select_by_visible_text('Banana')

## select by value 
#select.select_by_value('1')
#https://stackoverflow.com/questions/46553793/selecting-a-value-from-drop-down-with-span-id-in-selenium-python

=====
