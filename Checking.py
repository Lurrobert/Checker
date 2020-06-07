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


def nike(link, credentials):
    browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver')
    browser.get(link)
    time.sleep(2)
    credentials = list(credentials.values())
    #  Finding shoes
    size = credentials[-1]
    shoes = browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(size))
    browser.execute_script("arguments[0].scrollIntoView(true);", shoes)
    shoes.click()
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
    browser.switch_to.frame(browser.find_element_by_class_name('paymentFrameApexx'))

    card_fields = ['card_number', 'expiry_month', 'expiry_year', 'cvv']
    second_forms = credentials[len(forms):-1]
    for card_field, fill in zip(card_fields, second_forms):
        form = browser.find_element_by_id(card_field)
        form.send_keys(fill)


    pay = browser.find_element_by_id('hostedPaymentsubmitBtn')
    pay.click()
    time.sleep(3)
    
    browser.switch_to.default_content()
    # PayPal
    # Paypal = browser.find_element_by_id('PayPalMark_option')
    # Paypal.click()
    # pp_continue = browser.find_element_by_id('PayPal_Continue')
    # pp_continue.click()
    # time.sleep(5)
    # #Payment PP
    # mail = browser.find_element_by_id('email')
    # mail.send_keys('Later@gmail.com')
    # next = browser.find_element_by_id('btnNext')
    # next.click()
    # time.sleep(3)
    # pswrd = browser.find_element_by_id('password')
    # pswrd.send_keys('Later')
    # pay_button = browser.find_element_by_id('btnLogin')
    # pay_button.click()

    time.sleep(10)
    browser.close()


def start(link, credentials, date_of_release):
    while 1:
        date = datetime.datetime.now()
        if date.day == date_of_release.day and date.month == date_of_release.month:
            break
        else:
            time.sleep(5)
    Parallel(n_jobs=-1)(delayed(nike)(link, i) for i in credentials)

#release_date = datetime.datetime(year=2020, month=6, day=7)
#ln = 'https://www.nike.com/ru/launch/t/air-max-95-split-style'
# d = [{
#     'Shipping_LastName': 'hello',
#     'Shipping_FirstName': 'Lol',
#     'Shipping_MiddleName': 'adfvav',
#     'Shipping_PostCode': '190000',
#     'Shipping_Region': 'Санкт-Петербург',
#     'Shipping_Address1': 'No matter',
#     'Shipping_Address2': 'Jasrvasv',
#     'Shipping_phonenumber': '9052318663',
#     'shipping_Email': 'advaodrv@gmail.com',
#     'idNumber': '1832090230',
#     'IdIssuingAuthority': 'odnfvoaernv',
#     'IdVatNumber': '123456789123',
#     'card_number': '4255123443211234',
#     'expiry_month': '05',
#     'expiry_year': '60',
#     'cvv': '212',
#     'Size': '42'
# },
#     {
#         'Shipping_LastName': 'two',
#         'Shipping_FirstName': 'oiadnfvoa',
#         'Shipping_MiddleName': 'sadfasdf',
#         'Shipping_PostCode': '190000',
#         'Shipping_Region': 'Санкт-Петербург',
#         'Shipping_Address1': 'No matter',
#         'Shipping_Address2': 'fndniovndo',
#         'Shipping_phonenumber': '9052318653',
#         'shipping_Email': 'advaodrv@gmail.com',
#         'idNumber': '1832090230',
#         'IdIssuingAuthority': 'odnfvoaernv',
#         'IdVatNumber': '123456789123',
#         'card_number': '4255123443211234',
#         'expiry_month': '07',
#         'expiry_year': '60',
#         'cvv': '212',
#         'Size': '42'
#     }
# ]  # credentials
#start(ln, d, release_date)
