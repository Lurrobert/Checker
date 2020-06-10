import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler
import requests
import schedule 
import time
import logging
from requests.exceptions import ConnectionError
from uuid import uuid4

tok='1194379393:AAG9NZwGoQZp8pdr_RkrHS9T8Ae_5vOkN64'
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
    
def receiving_data(update, context):
    message = str(update.message.text).splitlines()
    context.user_data['link']=message[0]
    context.user_data['release_date']=message[1]
    context.user_data['credentials']=message[2].split(';')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=str(message[0], message[2]))
    
data_receiver = MessageHandler(Filters.text, receiving_data)
dispatcher.add_handler(data_receiver)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()