import logging
from telegram import TelegramError
from telegram.ext import *
import locate
import weather

def start(update, context):
    update.message.reply_text('Type something to get started')

def help(update, context):
    update.message.reply_text('This is a smiple bot for Blinds :)')

def error_handler(update, context):
    logging.warning('Update "%s" caused error "%s"', update, context.error)
    
def handle_message(update, context):
    text= str(update.message.text).lower()
    response = resp(text)    
    update.message.reply_text(response)

if __name__ == '__main__':
    updater = Updater('6039261665:AAEjir-iIaEd45IkcPh__03TQD0J83eHZLU', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('letsgo', weather.exec()))
    dp.add_handler(CommandHandler('whereami', locate.exe()))
   # dp.add_handler(CommandHandler('object_start', obj_start))
   # dp.add_handler(CommandHandler('social', social))
   # dp.add_handler(CommandHandler('post', post))
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()

