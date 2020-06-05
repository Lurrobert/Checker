import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import schedule
import datetime
from joblib import Parallel, delayed

release_date = '05.06.2020 13:00'
ln = 'https://www.nike.com/ru/launch/t/air-max-90-pink-foam'

# When to run
while 1:
    date = datetime.datetime.now()
    if date.day == 5 and date.month == 6:
        break
    else:
        time.sleep(5)


def nike(link):
    browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver')
    browser.get(link)
    time.sleep(3)

    #  Finding the element
    test = browser.find_elements_by_xpath('//button[text()[contains(.,"US 8.5")]]')
    browser.execute_script("arguments[0].scrollIntoView(true);", test[0])
    test[0].click()
    time.sleep(3)

    # Finding cart
    add_to_cart = browser.find_element_by_css_selector('button[data-qa="add-to-cart"]')
    browser.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    add_to_cart.click()
    time.sleep(3)

    # going to cart
    browser.get('https://www.nike.com/ru/ru/cart')
    time.sleep(4)


    browser.close()


#  Running in parallel
n = 3

Parallel(n_jobs=-1)(delayed(nike)(ln) for i in range(n))
