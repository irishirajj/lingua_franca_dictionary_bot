from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler,Filters
import os
from string import punctuation
import telegram.ext
import requests
TOKEN=os.environ.get("TELEGRAM_ID")
def start(update,context):
    yourname=update.message.chat.first_name
    msg="Hello "+yourname+"! Welcome to Lingua Franca Dictionary Bot"
    context.bot.send_message(update.message.chat.id,msg)

def help(update, context):
    update.message.reply_text("""
    The following commands are available for you:

    /start -> Welcome Message
    /help -> This Message
    /find /search /get -> Used to find the meaning, examples, synonyms and antonyms of any word.
    /syno -> Used to search the synonyms of any word.
    /anto -> Used to search the antonyms of any word.
    /explain -> Used to search all data about a word.
    /contact -> For suggestions and bug reports 
    """)
def details(update,context):
    context.bot.send_message(update.message.chat.id,str(update))

def mimic(update,context):
    context.bot.send_message(update.message.chat.id,update.message.text)

def error(update,context):
    context.bot.send_message(update.message.chat.it, "OOps! Error encountered")

def main():
    updater=Updater(token=TOKEN)   #updater
    dp=updater.dispatcher          #dispatcher

    ###################   Handlers :
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("details", details))

    dp.add_handler(MessageHandler(Filters.text,mimic))

    dp.add_error_handler(error)

    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=os.environ.get("PORT",443),
                          url_path=TOKEN,
                          webhook_url="https://lingua-franca-dictionary-bot.herokuapp.com/"+TOKEN
                          )

    updater.idle()

if __name__=='__main__':
    main()
