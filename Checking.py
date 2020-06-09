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


def nike(credentials):
    PROXY = credentials['proxy']
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=http://%s' % PROXY)

    browser = webdriver.Chrome('/Users/rob/Programming/Checker/chromedriver')  # , chrome_options=chrome_options
    browser.get(credentials['link'])
    wait = WebDriverWait(browser, 10)
    # TODO maximum speed
    # Finding shoes
    size = credentials['size']
    try:
        shoes = wait.until(EL((By.XPATH, "//button[contains(text(),'{}')]".format(size))))
        browser.execute_script("arguments[0].scrollIntoView(true);", shoes)
        shoes.click()
    except:
        return

    # Finding cart
    # add_to_cart = browser.find_element_by_css_selector('button[data-qa="add-to-cart"]')
    add_to_cart = wait.until(EL((By.CSS_SELECTOR, 'button[data-qa="add-to-cart"]')))
    browser.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    time.sleep(2)
    add_to_cart.click()

    # going to cart
    wait.until(EL((By.CSS_SELECTOR, 'button[data-qa="checkout-link"]')))
    browser.get('https://www.nike.com/ru/ru/cart')

    # Make an order
    wait.until(EL((By.CSS_SELECTOR, 'div[data-automation="cart-item"')))
    buy_without_reg = wait.until(EL((By.CSS_SELECTOR, 'button[data-automation="guest-checkout-button"]')))
    buy_without_reg.click()

    #  Forms
    forms = ['Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
             'Shipping_PostCode', 'Shipping_Region', 'Shipping_Address1',
             'Shipping_Address2', 'Shipping_phonenumber',
             'shipping_Email', 'idNumber', 'IdIssuingAuthority',
             'IdVatNumber']
    for form in forms:
        f = wait.until(EL((By.ID, form)))
        f.send_keys(credentials[form])

    # Check the date
    checkbox = browser.find_element_by_class_name('checkbox-checkmark')
    checkbox.click()

    # Continue
    # billing = browser.find_element_by_id('shippingSubmit')
    billing = wait.until(EL((By.ID, 'shippingSubmit')))
    wait.until(EC.element_to_be_clickable((By.ID, 'shippingSubmit')))
    billing.click()

    time.sleep(0.1)

    # Submitting
    # button_submit = browser.find_element_by_id('billingSubmit')
    button_submit = wait.until(EL((By.ID, 'billingSubmit')))
    time.sleep(0.1)
    # wait.until(EL((By.CSS_SELECTOR, 'div[data-ajax-loading style="display: none;"]')))
    wait.until(EC.element_to_be_clickable((By.ID, 'billingSubmit')))
    button_submit.click()

    # card Payment

    fram = wait.until(EL((By.CLASS_NAME, 'paymentFrameApexx')))
    browser.switch_to.frame(fram)

    card_fields = ['card_number', 'expiry_month', 'expiry_year', 'cvv']
    # Delete on fast internet
    time.sleep(1)
    for field in card_fields:
        # f = browser.find_element_by_id(field)
        f = wait.until(EL((By.ID, field)))
        f.send_keys(credentials[field])

    pay = browser.find_element_by_id('hostedPaymentsubmitBtn')
    pay.click()

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

    time.sleep(15)
    browser.close()


def start(update, context, done_list):  # credentials
    credentials = context.user_data['credentials']

    check_list = []
    for credit in credentials:
        if (credit not in check_list) and (credit not in done_list):
            date = datetime.datetime.now()
            dor = credit['date'].split('.')
            if len(dor) > 3:
                date_of_release = datetime. \
                    datetime(year=int(dor[0]), month=int(dor[1]), day=int(dor[2]), hour=int(dor[3]))
                if date.day == date_of_release.day and date.month == date_of_release.month and date.hour == date_of_release.hour:
                    check_list.append(credit)
                    done_list.append(credit)
            else:
                date_of_release = datetime. \
                    datetime(year=int(dor[0]), month=int(dor[1]), day=int(dor[2]))
                if date.day == date_of_release.day and date.month == date_of_release.month:
                    check_list.append(credit)
                    done_list.append(credit)

    if check_list:
        Parallel(n_jobs=-1)(delayed(nike)(d) for d in check_list)

    return done_list
