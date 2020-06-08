import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler
import requests
import schedule
import time
import logging
from requests.exceptions import ConnectionError
from uuid import uuid4
import Checking
import datetime
from joblib import Parallel, delayed


tok = '1194379393:AAG9NZwGoQZp8pdr_RkrHS9T8Ae_5vOkN64'
bot = telegram.Bot(token=tok)
updater = Updater(token=tok, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Starting')
    context.user_data['credentials'] = []


def receiving_data(update, context):
    message = str(update.message.text).splitlines()
    # if we don't have data now
    values = message
    forms = ['link', 'date', 'size', 'Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
             'Shipping_PostCode',
             'Shipping_Region', 'Shipping_Address1', 'Shipping_Address2', 'Shipping_phonenumber',
             'shipping_Email', 'idNumber', 'IdIssuingAuthority', 'IdVatNumber', 'card_number',
             'expiry_month', 'expiry_year', 'cvv']

    context.user_data['credentials'].append(dict(zip(forms, values)))


def start_checking(update, context):
    credentials = context.user_data['credentials']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Running')
    Checking.start(credentials)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Everything is done')


def stoper(update, context):
    if str.lower(str(update.message.text)) == 'stop':
        print('working')
        updater.stop()
        updater.start_polling()



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

check_starter = CommandHandler('run', start_checking)
dispatcher.add_handler(check_starter)

# it should be last
data_receiver = MessageHandler(Filters.text, receiving_data)
dispatcher.add_handler(data_receiver)

updater.start_polling()
