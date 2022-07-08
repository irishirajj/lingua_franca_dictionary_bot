from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import os
import json
import requests

from string import punctuation
import telegram.ext

TOKEN = os.environ.get("TELEGRAM_ID")
app_id = os.environ.get("OXFORD_APP_ID")
app_key = os.environ.get("OXFORD_APP_KEY")


def start(update, context):
    yourname = update.message.chat.first_name
    msg = "Hello " + yourname + "! Welcome to Lingua Franca Dictionary Bot"
    context.bot.send_message(update.message.chat.id, msg)


def help(update, context):
    update.message.reply_text("""
    The following commands are available for you:

    /start -> Welcome Message
    /help -> This Message
    /find /search /look -> Used to find the meaning, examples, synonyms and antonyms of any word.
    /syno -> Used to search the synonyms of any word.
    /anto -> Used to search the antonyms of any word.
    /explain -> Used to search all data about a word.
    /contact -> For suggestions and bug reports 
    """)


def anto(update, context):
    msg = f"{update.message.text}"
    word = msg[6:]
    antonyms = antoList(word)
    if (len(antonyms) == 0):
        update.message.reply_text("Sorry! The word was not found in our dictionary.")
        return ""
    word = "<b>" + word[0].upper() + word[1:] + "</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + word + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n" + antonyms
    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)


def antoList(word):
    url = f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key=06a00f95-9843-4f0f-9378-dec4f507c81b"
    jeasons = requests.get(url).json()
    if (len(jeasons) == 0):
        return
    if (type(jeasons[0]) == str):
        return
    antonyms = set()
    lenjeasons = len(jeasons)
    for i in range(lenjeasons):
        jeason_i = jeasons[i]
        if (jeason_i.__contains__('meta')):
            meta_i = jeason_i['meta']
            if (meta_i.__contains__('ants')):
                ants_i = meta_i['ants']
                len_ants_i = len(ants_i)
                for j in range(len_ants_i):
                    ants_i_j = ants_i[j]
                    len_ants_i_j = len(ants_i_j)
                    for k in range(len_ants_i_j):
                        antonyms.add(ants_i_j[k])
    final_antonym_list = ""
    #n = len(antonyms)
    #for i in range(n):
    #    final_antonym_list += antonyms[i + 1]
    #    if i != n - 1:
    #        final_antonym_list += ", "
    for antonym in antonyms:
        final_antonym_list += antonym +", "
    return final_antonym_list

def syno(update, context):
    msg = f"{update.message.text}"
    word = msg[6:]
    synonyms = synoList(word)
    if (len(synonyms) == 0):
        update.message.reply_text("Sorry! The word was not found in our dictionary.")
        return ""
    word = "<b>" + word[0].upper() + word[1:] + "</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + word + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonyms
    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)

def synoList(word):
    language = 'en-gb'
    strictMatch = 'false'
    fields2 = 'synonyms'
    oxTheUrl = 'https://od-api.oxforddictionaries.com:443/api/v2/thesaurus/' + language + '/' + word.lower() + '?fields=' + fields2 + '&strictMatch=' + strictMatch;
    r = requests.get(oxTheUrl, headers={'app_id': app_id, 'app_key': app_key})
    # print(r.status_code)
    if (r.status_code != 200):
        return ""
    json_load = r.json()
    list = json_load['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]
    synonyms = list['synonyms']
    mysyno = "1. "
    length = len(synonyms)
    for i in range(length):
        if (i == 0):
            mysyno += "<b>" + synonyms[i]['text'] + "</b>, "
        elif (i == length - 1):
            mysyno += synonyms[i]['text'] + " "
        else:
            mysyno += synonyms[i]['text'] + ", "
    mysyno += "\n"
    if (list.__contains__('subsenses')):
        newlist = list['subsenses']
        listLength = len(newlist)
        for i in range(listLength):
            mysyno += str(i + 2) + ". "
            synonyms = newlist[i]['synonyms']
            length = len(synonyms)
            for j in range(length):
                if (j == 0):
                    mysyno += "<b>" + synonyms[j]['text'] + "</b>, "
                elif (j == length - 1):
                    mysyno += synonyms[j]['text'] + " "
                else:
                    mysyno += synonyms[j]['text'] + ", "
            mysyno += "\n"
    return mysyno

def findAudioUrl(jeasons,word):
    audioname = jeasons[0]['hwi']['prs'][0]['sound']['audio']
    subdir = ""
    if (audioname[0:2] == "bix"):
        subdir = "bix"
    elif (audioname[0:1] == "gg"):
        subdir = "gg"
    elif ((audioname[0].isdigit()) or (audioname[0] in punctuation)):
        subdir = "number"
    else:
        subdir = audioname[0]
    audiourl = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{audioname}.mp3"


def find(update,context):
    msg = f"{update.message.text}"
    word = msg[6:]
    word=word.lower()
    # Access the dictionary Merriam Webster dictionary for definition and pronunciation
    urldict = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=1f6a028a-e36e-4742-86f9-d087462e185e"
    #url    = f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key=06a00f95-9843-4f0f-9378-dec4f507c81b"
    r = requests.get(urldict)
    meandict=r.json()
    if (len(meandict) == 0):
        update.message.reply_text("Sorry! The word was not found in our dictionary.")
        return
    if (type(meandict[0]) == str):
        update.message.reply_text("Sorry! The word was not found in our dictionary.")
        return

    #audiourl=findAudioUrl(meandict,word)

    word = "<b>" + word[0].upper() + word[1:].lower() + "</b>"

    shortDefinitions=meandict[0]['shortdef']
    len_shortDefinitions = len(shortDefinitions)
    shortdef=""
    for i in range(len_shortDefinitions):
        shortdef += shortDefinitions[i]+"; "
    parts_of_speech = meandict[0]['fl']

    mysyno=synoList(word)
    ants=antoList(word)
    example = giveOneExample(word)

    update.message.reply_text(mysyno)
    update.message.reply_text(ants)
    update.message.reply_text(example)
    update.message.reply_text(parts_of_speech)
    update.message.reply_text("LIFE IS A RACE and YOU ARE ANDA", parse_mode=telegram.ParseMode.HTML)
    return



    strng = u"\U0001F1EE\U0001F1F3" + " " + word + " ," + parts_of_speech + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + shortdef + "\n\n" + u"\U0001F4DA <b>Example</b> :\n"+example
    strng += "\n\n" + u"\U0001F4D7 <b>Synonyms</b> :\n" + mysyno + "\n\n" + u"\U0001F4D7 <b>Antonyms</b> :\n" + ants


    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
    #gupdate.message.reply_audio(audiourl, caption=f"Pronunciation of <b>{word.lower()} </b>",
                               #parse_mode=telegram.ParseMode.HTML)



def giveOneExample(word):
    language = 'en-gb'
    word_id = word
    strictMatch = 'false'
    test=f"https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{word_id}?strictMatch=false"
    r=requests.get(test, headers = {'app_id': app_id, 'app_key': app_key})
    #print(r.status_code)
    if(r.status_code!=200):
        return ""
    testr=r.json()
    le=testr['results'][0]['lexicalEntries']
    le_0=le[0]
    sense_0=le_0['entries'][0]['senses'][0]
    if(sense_0.__contains__('examples')):
        example=sense_0['examples'][0]['text']
        return example
    return ""


def details(update, context):
    context.bot.send_message(update.message.chat.id, str(update))


def mimic(update, context):
    context.bot.send_message(update.message.chat.id, update.message.text)


def error(update, context):
    context.bot.send_message(update.message.chat.id, "OOps! Error encountered")


def main():
    updater = Updater(token=TOKEN)  # updater
    dp = updater.dispatcher  # dispatcher

    ###################   Handlers :
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("anto", anto))
    dp.add_handler(CommandHandler("syno", syno))
    dp.add_handler(CommandHandler("find", find))
    #dp.add_handler(CommandHandler("search", find))
    #dp.add_handler(CommandHandler("look", find))

    dp.add_handler(CommandHandler("details", details))

    dp.add_handler(MessageHandler(Filters.text, mimic))

    dp.add_error_handler(error)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=os.environ.get("PORT", 443),
                          url_path=TOKEN,
                          webhook_url="https://lingua-franca-dictionary-bot.herokuapp.com/" + TOKEN
                          )

    updater.idle()


if __name__ == '__main__':
    main()
