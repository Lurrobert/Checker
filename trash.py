from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.select import Select


browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver')
browser.get('http://localhost:63342/Checker/test.html?_ijt=ea6e96kk46re3vggn9pedlt3ak')
form = browser.find_element_by_id('pet-select')
select = Select(form)
select.select_by_visible_text('Dog')
