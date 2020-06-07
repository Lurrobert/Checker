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
    context.user_data['release_date'] = []
    context.user_data['link'] = []
    context.user_data['credentials'] = []


def receiving_data(update, context):
    message = str(update.message.text).splitlines()
    # if we don't have data now
    if not context.user_data['release_date']:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='adding new')
        try:
            context.user_data['link'] = message[0]
            # TODO add checking format of link and date
            dt = message[1].split('.')
            context.user_data['release_date'] = datetime.datetime(year=int(dt[0]), month=int(dt[1]), day=int(dt[2]))
        except:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Wrong format. Try again')
    else:
        values = message
        forms = ['Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName', 'Shipping_PostCode',
                 'Shipping_Region', 'Shipping_Address1', 'Shipping_Address2', 'Shipping_phonenumber',
                 'shipping_Email', 'idNumber', 'IdIssuingAuthority', 'IdVatNumber', 'card_number',
                 'expiry_month', 'expiry_year', 'cvv', 'Size']

        context.user_data['credentials'].append(dict(zip(forms, values)))


def start_checking(update, context):
    link = context.user_data['link']
    release_date = context.user_data['release_date']
    credentials = context.user_data['credentials']
    Checking.start(link, credentials, release_date)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

check_starter = CommandHandler('run', start_checking)
dispatcher.add_handler(check_starter)

# it should be last
data_receiver = MessageHandler(Filters.text, receiving_data)
dispatcher.add_handler(data_receiver)

updater.start_polling()
