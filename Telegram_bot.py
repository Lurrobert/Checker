import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler
import time
import logging
from uuid import uuid4
import Checking
import datetime
from joblib import Parallel, delayed
from multiprocessing import Pool
from multiprocessing import Process
from telegram.ext.dispatcher import run_async
import os
import sys
from threading import Thread
import threading

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


def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


def restart(update, context):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()
    print('started')


def receiving_data(update, context):
    message = update.message.text.splitlines()
    values = message
    forms = ['link', 'proxy', 'date', 'size', 'Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
             'Shipping_PostCode',
             'Shipping_Region', 'Shipping_Address1', 'Shipping_Address2', 'Shipping_phonenumber',
             'shipping_Email', 'idNumber', 'IdIssuingAuthority', 'IdVatNumber', 'card_number',
             'expiry_month', 'expiry_year', 'cvv']

    context.user_data['credentials'].append(dict(zip(forms, values)))


@run_async
def start_checking(update, context):
    done_list = []

    credentials = context.user_data['credentials']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Running')

    while context.user_data['credentials'][-1]['link'] != 'stop':
        done_list = Checking.start(update, context, done_list)

        if len(done_list) == len(credentials):
            break
        time.sleep(0.01)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='DONE')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

check_starter = CommandHandler('run', start_checking)
dispatcher.add_handler(check_starter)

dispatcher.add_handler(CommandHandler('stop', restart))

# it should be last
data_receiver = MessageHandler(Filters.text, receiving_data)
dispatcher.add_handler(data_receiver)

updater.start_polling()
