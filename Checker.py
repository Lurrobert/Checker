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


release_date = '05.06.2020 13:00'
ln = 'https://www.nike.com/ru/launch/t/air-max-90-pink-foam'

# When to run
while 1:
    date = datetime.datetime.now()
    if date.day == 5 and date.month == 6:
        break
    else:
        time.sleep(5)


def nike(link, data):
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

    #  Form

    # Name
    # surname = browser.find_element_by_id('Shipping_LastName')
    # name = browser.find_element_by_id('Shipping_FirstName')
    # middle_name = browser.find_element_by_id('Shipping_MiddleName')
    # # Address
    # post_code = browser.find_element_by_id('Shipping_PostCode') # May be problems
    # region = browser.find_element_by_id('Shipping_Region') #197001
    # select = Select(region)
    # time.sleep(1)
    # select.select_by_visible_text('Санкт-Петербург')
    # house1 = browser.find_element_by_id('Shipping_Address1')
    # house2 = browser.find_element_by_id('Shipping_Address2')
    # phone = browser.find_element_by_id('Shipping_phonenumber')

    forms = ['Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
             'Shipping_PostCode', 'Shipping_Region', 'Shipping_Address1',
             'Shipping_Address2', 'Shipping_phonenumber',
             'shipping_Email', 'idNumber', 'IdIssuingAuthority',
             'IdVatNumber']

    data = list(data.values())
    first_forms = data[:len(forms)]
    time.sleep(5)
    for name, fill in zip(forms, first_forms):  # make zip and iterate
        form = browser.find_element_by_id(name)
        form.send_keys(fill)
        # if name == 'Shipping_Region':  # 197001
        #     select = Select(form)
        #     time.sleep(1)
        #     select.select_by_visible_text('Санкт-Петербург')
        #
        # if name == 'Shipping_PostCode':
        #     form.send_keys(190000)
        #     browser.execute_script("arguments[0].scrollIntoView(true);",
        #                            browser.find_element_by_id('idNumber'))
        #     time.sleep(1)
        #
        # else:
        #     form.send_keys('Checking')
        #     time.sleep(2)

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
    card_fields = ['card_number', 'expiry_month', 'expiry_year', 'cvv']
    second_forms = data[len(forms):]
    for card_field, fill in zip(card_fields, second_forms):
        form = browser.find_element_by_id(card_field)
        form.send_keys(fill)

    time.sleep(10)
    browser.close()


#  Running in parallel
n = 1

d = {
    'Shipping_LastName': 'hello',
    'Shipping_FirstName': 'Lol',
    'Shipping_MiddleName': 'adfvav',
    'Shipping_PostCode': '190000',
    'Shipping_Region': 'Санкт-Петербург',
    'Shipping_Address1': 'No matter',
    'Shipping_Address2': 'Jasrvasv',
    'Shipping_phonenumber': '9052318663',
    'shipping_Email': 'advaodrv@gmail.com',
    'idNumber': '1832090230',
    'IdIssuingAuthority': 'odnfvoaernv',
    'IdVatNumber': '123456789123',
    'card_number': '4255123443211234',
    'expiry_month': '05',
    'expiry_year': '60',
    'cvv': '212'
}

Parallel(n_jobs=-1)(delayed(nike)(ln, d) for i in range(n))  # Можно передать i как параметр для разных акков
