import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import schedule
import datetime
from joblib import Parallel, delayed
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from joblib import Parallel, delayed
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import presence_of_element_located as EL

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('window-size=1920x1480')

browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver', chrome_options=chrome_options)

browser.get('http://localhost:63342/Checker/worker.html?_ijt=4gubqq0ibsjdvm83qgm07fos78')
browser.find_element_by_id('hello').click()
print(browser.current_url)
