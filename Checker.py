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


def nike(link, credentials, release_date):

    while 1:
        date = datetime.datetime.now()
        if date.day == release_date.day and date.month == release_date.month:
            break
        else:
            time.sleep(5)

    link = link
    credentials = credentials
    browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver')
    browser.get(link)
    time.sleep(2)

    #  Finding the element
    test = browser.find_elements_by_xpath('//button[text()[contains(.,"US 8.5")]]')
    browser.execute_script("arguments[0].scrollIntoView(true);", test[0])
    test[0].click()
    time.sleep(2)

    # Finding cart
    add_to_cart = browser.find_element_by_css_selector('button[data-qa="add-to-cart"]')
    browser.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    add_to_cart.click()
    time.sleep(2)

    # going to cart
    browser.get('https://www.nike.com/ru/ru/cart')

    # Make an order
    time.sleep(5)
    buy_without_reg = browser.find_element_by_css_selector('button[data-automation="guest-checkout-button"]')
    buy_without_reg.click()

    #  Forms
    forms = ['Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
             'Shipping_PostCode', 'Shipping_Region', 'Shipping_Address1',
             'Shipping_Address2', 'Shipping_phonenumber',
             'shipping_Email', 'idNumber', 'IdIssuingAuthority',
             'IdVatNumber']

    credentials = list(credentials.values())
    first_forms = credentials[:len(forms)]
    time.sleep(5)
    for name, fill in zip(forms, first_forms):  # make zip and iterate
        form = browser.find_element_by_id(name)
        form.send_keys(fill)

    # Check the date
    checkbox = browser.find_element_by_class_name('checkbox-checkmark')
    checkbox.click()

    # Continue
    time.sleep(4)
    billing = browser.find_element_by_id('shippingSubmit')
    billing.click()

    # Submitting
    time.sleep(5)
    button_submit = browser.find_element_by_id('billingSubmit')
    button_submit.click()
    time.sleep(8)

    # card Payment
    # card_fields = ['card_number', 'expiry_month', 'expiry_year', 'cvv']
    # second_forms = data[len(forms):]
    # for card_field, fill in zip(card_fields, second_forms):
    #     form = browser.find_element_by_id(card_field)
    #     form.send_keys(fill)

    time.sleep(10)
    browser.close()

