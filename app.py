from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler,Filters
import os
import json
import requests

from string import punctuation
import telegram.ext

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
def anto(update,context):
    msg = f"{update.message.text}"
    word = msg[6:]
    antonyms = antoList(word)
    if( len(antonyms) == 0):
        update.message.reply_text("Sorry! The word was not found in our dictionary.")
        return ""
    word = "<b>"+word[0].upper()+word[1:]+"</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + word + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n" + antonyms

def antoList(word):
    url = f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key=06a00f95-9843-4f0f-9378-dec4f507c81b"
    jeasons= requests.get(url).json()
    if(len(jeasons)==0):
        return
    if(type(jeasons[0])==str):
        return
    antonyms=set()
    lenjeasons=len(jeasons)
    for i in range(lenjeasons):
        jeason_i=jeasons[i]
        if (jeason_i.__contains__('meta')):
            meta_i=jeason_i['meta']
            if (meta_i.__contains__('ants')):
                ants_i=meta_i['ants']
                len_ants_i=len(ants_i)
                for j in range(len_ants_i):
                    ants_i_j=ants_i[j]
                    len_ants_i_j=len(ants_i_j)
                    for k in range(len_ants_i_j):
                        antonyms.add(ants_i_j[k])
    final_antonym_list=""
    n=len(antonyms)
    if(n>0):
        final_antonym_list +=antonyms[0]
    for i in range(n-1):
        final_antonym_list+=", "+antonyms[i+1]

    return final_antonym_list



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
