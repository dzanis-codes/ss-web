from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get('url')

select = Select(driver.find_element_by_id('fruits01'))

# select by visible text
select.select_by_visible_text('Banana')

# select by value 
select.select_by_value('1')

=====

from selenium import webdriver
from selenium.webdriver.support.ui import Select

b = webdriver.Firefox()

# navigate to the page
select = Select(b.find_element_by_id(....))
print select.options
print [o.text for o in select.options] # these are string-s
select.select_by_visible_text(....)
