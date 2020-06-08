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
from multiprocessing import Pool
import ray
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
    print(update.message.text)
    message = update.message.text.splitlines()
    values = message
    forms = ['link', 'date', 'size', 'Shipping_LastName', 'Shipping_FirstName', 'Shipping_MiddleName',
             'Shipping_PostCode',
             'Shipping_Region', 'Shipping_Address1', 'Shipping_Address2', 'Shipping_phonenumber',
             'shipping_Email', 'idNumber', 'IdIssuingAuthority', 'IdVatNumber', 'card_number',
             'expiry_month', 'expiry_year', 'cvv']

    context.user_data['credentials'].append(dict(zip(forms, values)))


@run_async
def start_checking(update, context):
    print(threading.active_count())
    credentials = context.user_data['credentials']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Running')
    # Checking.start(update, context)

    # NEW
    # done_list = []
    # while update.message.text != 'stop':
    #     check_list = []
    #     for credit in credentials:
    #         if (credit not in check_list) and (credit not in done_list):
    #             date = datetime.datetime.now()
    #             dor = credit['date'].split('.')
    #             if len(dor) > 3:
    #                 date_of_release = datetime. \
    #                     datetime(year=int(dor[0]), month=int(dor[1]), day=int(dor[2]), hour=int(dor[3]))
    #                 if date.day == date_of_release.day and date.month == date_of_release.month and date.hour == date_of_release.hour:
    #                     check_list.append(credit)
    #                     done_list.append(credit)
    #             else:
    #                 date_of_release = datetime. \
    #                     datetime(year=int(dor[0]), month=int(dor[1]), day=int(dor[2]))
    #                 if date.day == date_of_release.day and date.month == date_of_release.month:
    #                     check_list.append(credit)
    #                     done_list.append(credit)
    #     if check_list:
    #         Parallel(n_jobs=-1)(delayed(Checking.nike)(d) for d in check_list)
    #
    #     if len(done_list) == len(credentials):
    #         break
    #
    #     time.sleep(60)
    # End

    #NEW2

    done_list = []
    while context.user_data['credentials'][-1]['link'] != 'stop':
        done_list = Checking.start(update, context, done_list)

        if len(done_list) == len(credentials):
            break
        time.sleep(10)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Stopped')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

check_starter = CommandHandler('run', start_checking)
dispatcher.add_handler(check_starter)

dispatcher.add_handler(CommandHandler('stop', restart))

# it should be last
data_receiver = MessageHandler(Filters.text, receiving_data)
dispatcher.add_handler(data_receiver)

updater.start_polling()
