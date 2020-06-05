import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import schedule
import datetime
from joblib import Parallel, delayed


#  Getting link and opening browser


def nike(link):
    browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver')
    browser.get(link)

    # b = []
    # for i in range(n):
    #     b.append(webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver'))
    #     b[i].get(link)
    #
    # for p in range(n):
    #     size = b[p].find_elements_by_xpath('//button[text()[contains(.,"US 8.5")]]')
    #     b[p].execute_script("arguments[0].scrollIntoView(true);", size[0])
    #     size[0].click()

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


#  We can automate it too
release_date = '05.06.2020 13:00'
l = 'https://www.nike.com/ru/launch/t/air-max-90-pink-foam'

# When to run
while 1:
    date = datetime.datetime.now()
    if date.day == 5 and date.month == 6:
        break
    else:
        time.sleep(5)

Parallel(n_jobs=-1)(delayed(nike)(l) for n in range(3))
