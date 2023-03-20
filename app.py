import telegram
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests,json

bot = telegram.Bot(token='6039261665:AAEjir-iIaEd45IkcPh__03TQD0J83eHZLU')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a simple bot. How can I help you?")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command check /help to know more")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="List of all commands: \n 1. /whereami  - Current Location\n 2. /letsgo  - Check whether before you go \n 3. /start  - Description of the bot \n 4. /help  - List of all commands")


def letsgo(update, context):
    api_endpoint = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "8927948f22cdd28e1fc7562a80631900"
    location = "Chennai"
    params = {"q": location,"appid": api_key,"units": "metric"}
    response = requests.get(api_endpoint, params=params)
    data = json.loads(response.text)
    wind_speed = data["wind"]["speed"]
    telegram_endpoint = "https://api.telegram.org/bot6039261665:AAEjir-iIaEd45IkcPh__03TQD0J83eHZLU/sendMessage"

    if (wind_speed > 5):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Don't go outside the wind is high")
    if(wind_speed < 5):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Yes its good to go outside right now")

        
def whereami(update,context):
    int_med = 'https://ipapi.co/'+str(request.headers.get('X-Forwarded-For', request.remote_addr))+'/json'
    response = requests.get(int_med)
    location = response.json()

    lat = location['latitude']
    longitude = location['longitude']
    loc = location['city']
    out = "Latitude : " + str(lat) + "\n" + "Longitude : " + str(longitude) + "\n" + "Location : " + str(loc)
    print(out)
    context.bot.send_message(chat_id=update.effective_chat.id, text=out)

    
updater = Updater(token='6039261665:AAEjir-iIaEd45IkcPh__03TQD0J83eHZLU', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
updater.dispatcher.add_handler(CommandHandler('letsgo', letsgo))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('whereami', whereami))

updater.start_polling()
