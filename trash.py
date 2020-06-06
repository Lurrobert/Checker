import datetime
import time

from joblib import Parallel, delayed

from Checker import nike

t = '05.06.2020 13:00'
release_date = datetime.datetime(year=2020, month=6, day=6)
ln = 'https://www.nike.com/ru/launch/t/air-max-90-pink-foam'

d = [{
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
},
    {
        'Shipping_LastName': 'two',
        'Shipping_FirstName': 'oiadnfvoa',
        'Shipping_MiddleName': 'sadfasdf',
        'Shipping_PostCode': '190000',
        'Shipping_Region': 'Санкт-Петербург',
        'Shipping_Address1': 'No matter',
        'Shipping_Address2': 'fndniovndo',
        'Shipping_phonenumber': '9052318653',
        'shipping_Email': 'advaodrv@gmail.com',
        'idNumber': '1832090230',
        'IdIssuingAuthority': 'odnfvoaernv',
        'IdVatNumber': '123456789123',
        'card_number': '4255123443211234',
        'expiry_month': '07',
        'expiry_year': '60',
        'cvv': '212'
    }
]  # credentials

Parallel(n_jobs=-1)(delayed(nike)(ln, i, release_date) for i in d)
