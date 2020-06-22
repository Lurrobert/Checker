import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import datetime
from joblib import Parallel, delayed
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from joblib import Parallel, delayed
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import presence_of_element_located as presense_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

max_retry = 5

class Nike:

    def __init__(self, credentials):
        self.credentials = credentials
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True
        options = Options()
        options.headless = False
        options.add_argument("--window-size=1920,1080")
        cap["pageLoadStrategy"] = "eager"
        # options.proxy = credentials['proxy']
        self.browser = webdriver.Firefox(executable_path='Drivers/geckodriver',
                                         desired_capabilities=cap, options=options)
        self.wait = WebDriverWait(self.browser, 5)
        self.browser.get(credentials['link'])

    def login(self):
        user = self.credentials['user']
        pasw = self.credentials['pasw']
        self.browser.get(self.credentials['link'])
        retry = 0
        while True:
            try:
                retry += 1
                b = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/ul/li['
                               '1]/button')))
                b.click()

                a = self.wait.until(EC.visibility_of_element_located((By.NAME, 'emailAddress')))
                b = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
                a.send_keys(user)
                b.send_keys(pasw)

                go = self.wait.until(presense_located((By.CSS_SELECTOR, 'input[type="button"]')))
                go.click()
                time.sleep(3)

                try:
                    self.browser.find_element_by_class_name("nike-unite-error-panel")

                    print('Exception  logging in retry ' + str(retry))
                    self.browser.get(self.credentials['link'])

                    if retry > max_retry:
                        print('Error in user login page  - ' + str(user))
                        return


                except:
                    print('Logged in')
                    break

            except:
                print('Exception  logging in retry ' + str(retry))
                self.browser.save_screenshot("snapshots/login-error.png")
                if retry > max_retry:
                    print('Error in user login page  - ' + str(user))
                    return

    def availability(self):
        size = self.credentials['size']
        while True:
            try:
                self.browser.refresh()
                shoes = self.wait.until(presense_located((By.XPATH, "//button[contains(text(),'{}')]".format(size))))
                self.browser.execute_script("arguments[0].scrollIntoView(true);", shoes)
                shoes.click()
                print('Shoes chosen')
                break
            except Exception:
                print('No shoes')

    def add_to_cart(self):
        retry = 0
        while True:
            try:
                retry += 1
                add_to_cart = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="add-to-cart"]')))
                self.browser.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
                add_to_cart.click()
                try:
                    self.browser.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div/div/div[2]')
                    print('added')
                    break
                except:
                    try:
                        self.browser.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/ul/li[3]/a/span')
                        print('added to cart')
                        break
                    except:
                        print('cart Empty')
                        if retry > max_retry:
                            print('Too much errors')
                            return

            except Exception:
                print('Cart error')
                if retry > max_retry:
                    print('Too much errors')
                    break


    def nike(self):
        tic = time.time()

        credentials = self.credentials

        # Finding cart
        add_to_cart = self.wait.until(presense_located((By.CSS_SELECTOR, 'button[data-qa="add-to-cart"]')))
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="add-to-cart"]')))
        self.browser.execute_script("arguments[0].scrollIntoView(true);", shoes)
        add_to_cart.click()
        time.sleep(1)
        try:
            self.wait.until(presense_located((By.CSS_SELECTOR, 'button[data-qa="checkout-link"]')))
        except:
            print('exception')
            add_to_cart.click()

        self.browser.get('https://www.nike.com/ru/ru/cart')

        # Make an order
        self.wait.until(presense_located((By.CSS_SELECTOR, 'div[data-automation="cart-item"')))
        buy_without_reg = self.wait.until(presense_located((By.XPATH, '//*[@id="maincontent"]/div[2]/div[2]/aside/div['
                                                                      '5]/div/button[1]')))
        buy_without_reg.click()
        print('Bought')
        #  Forms
        forms = ['Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
                 'Shipping_PostCode', 'Shipping_Region', 'Shipping_Address1',
                 'Shipping_Address2', 'Shipping_phonenumber',
                 'shipping_Email', 'idNumber', 'IdIssuingAuthority',
                 'IdVatNumber']
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'Shipping_LastName')))
        except:
            time.sleep(2)

        for form in forms:
            f = self.wait.until(EC.element_to_be_clickable((By.ID, form)))
            f.send_keys(credentials[form])

        print('Formed')

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'checkbox-checkmark')))
        a = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'checkbox-checkmark')))
        self.browser.execute_script("arguments[0].scrollIntoView(true);", a)
        try:
            a.click()
        except:
            time.sleep(2)
            a.click()

        # Continue

        billing = self.wait.until(presense_located((By.ID, 'shippingSubmit')))
        self.browser.execute_script("arguments[0].scrollIntoView(true);", billing)
        billing.click()

        # Submitting

        button_submit = self.wait.until(presense_located((By.ID, 'billingSubmit')))
        self.wait.until(EC.element_to_be_clickable((By.ID, 'billingSubmit')))
        button_submit.click()

        # card Payment

        fram = self.wait.until(presense_located((By.CLASS_NAME, 'paymentFrameApexx')))
        self.browser.switch_to.frame(fram)

        card_fields = ['card_number', 'expiry_month', 'expiry_year', 'cvv']
        # Delete on fast internet
        for field in card_fields:
            f = self.wait.until(EC.visibility_of_element_located((By.ID, field)))
            f.send_keys(credentials[field])

        pay = self.browser.find_element_by_id('hostedPaymentsubmitBtn')
        pay.click()

        self.browser.switch_to.default_content()
        tac = time.time()
        print(tac - tic)
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
        print('DONE')
        time.sleep(20)
        self.browser.close()

    def start(self, update, context, done_list):  # credentials
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

        print('checking ', len(check_list))
        if check_list:
            Parallel(n_jobs=-1)(delayed(self.nike)(d) for d in check_list)

        return done_list
