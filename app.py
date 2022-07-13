from telegram.ext import Updater, filters
from telegram.ext import CommandHandler, MessageHandler, Filters
import os
import json
import requests

from string import punctuation
import telegram.ext

import myfile
import mapfile
admins = [-623259517,-1001699888041,-1001523164933,5310284596]
# ,2060060048

TOKEN = os.environ.get("TELEGRAM_ID")
app_id = os.environ.get("OXFORD_APP_ID")
app_key = os.environ.get("OXFORD_APP_KEY")
merriam_dict_key=os.environ.get("MERRIAM_DICT_KEY")

def start(update, context):
    yourname = update.message.from_user.first_name
    msg = "Hello " + yourname + "! Welcome to Lingua Franca Dictionary Bot"

    #context.ext.filters.ChatType.PRIVATE.bot.send_message(update.message.chat.id, msg)
    #PRIVATE = filters.ChatType.PRIVATE
    #PRIVATE.bot.send_message(update.message.chat.id,msg)
    context.bot.send_message(update.message.chat.id, msg)


def help(update, context):
    update.message.reply_text("""
    The following commands are available for you:

    /start -> Welcome Message
    /help ->  All commands
    /find /search /look -> Find the meaning, examples, synonyms and antonyms of any word.
    /syno -> Search the synonyms of any word.
    /anto -> Search the antonyms of any word.
    /explain -> All data about a word.
    /contact -> For suggestions and bug reports 
    """)

def searchall(update, context):
    if update.message.chat.id not in admins:
        ans = "To be used in the group Lingua Franca English House (<a href='https://t.me/+xeg0uDpOFfE4MTJl'>t.me/+xeg0uDpOFfE4MTJl </a>). Join the group if you haven't already thanks 😊😊."
        update.message.reply_text(ans, parse_mode=telegram.ParseMode.HTML)
        return
    msg = f"{update.message.text}".lower()
    language = 'en-gb'
    word_id = msg[11:]
    if (word_id == "lingua franca"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper()+word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n"+ "a language used for communication between groups of people who speak different languages" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "The international business community sees English as a lingua franca."+ "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word_id == "meghna"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper()+word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n"+ "Thunder; Also used to refer the holy river Goddess Ganga; One of the best singers" +  "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" +"Thuder, Lightning, Ganges, Holy, Pretty, Beautiful, Melodious, Buddy:), Awesome, Fantastic, Endearing, Best Singer, Best Buddy,"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word_id=="jo"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper() + word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "A sweetheart; Beloved one; Dear(often used in addressing a person)" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "I thought it might have been one of the servant girls with her jo.\n Oh you're a jo, she said, when I brought her breakfast in bed." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\nSweetheart"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word_id == "rishi"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper()+word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n"+ "A holy Hindu sage; Saint, Inspired poet" +  "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" +"Rishi, IRun Man, Deep Learning, Dark Warrior, Artist, Developer, Engineer"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return

    #UPDATE THE COUNT ::::::::----->>>
    initial_count=myfile.x
    final_count=initial_count+3
    myfile.x=final_count

    find3(update, context)
    strictMatch = 'false'
    test = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{word_id}?strictMatch=false"
    r = requests.get(test, headers={'app_id': app_id, 'app_key': app_key})
    # print(r.status_code)
    if (r.status_code != 200):
        #update.message.reply_text("Sorry! The word was not found in our dictionary.")
        return
    testr = r.json()
    le = testr['results'][0]['lexicalEntries']
    for i in range(len(le)):  # i is representing the number of the lexical entry
        le_i = le[i]
        pos = le_i['lexicalCategory']['text']
        entries = le_i['entries']
        senses = entries[0]['senses']
        for j in range(len(senses)):
            sense_j = senses[j]

            definition = ""
            if (sense_j.__contains__('definitions')):
                definitions = sense_j['definitions']
                for k in range(len(definitions)):
                    definition += definitions[k] + "; "

            example = ""
            if (sense_j.__contains__('examples')):
                examples = sense_j['examples']
                for k in range(len(examples)):
                    example += str(k + 1) + ". "
                    example += examples[k]['text'][0].upper()+examples[k]['text'][1:].lower() + "\n"

            synonym = ""
            if (sense_j.__contains__('synonyms')):
                synonyms = sense_j['synonyms']
                for k in range(len(synonyms)):
                    synonym += synonyms[k]['text'] + "; "

            word = "<b>" + msg[11].upper() + msg[12:].lower() + "</b>"
            strng = u"\U0001F1EE\U0001F1F3" + " " + word + " ," + pos + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + definition + "\n\n" + u"\U0001F4DA <b>Examples</b> :\n" + example + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonym
            update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)

def find3(update, context):
    msg = f"{update.message.text}"
    word=msg[11:].lower()
    merriam_url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={merriam_dict_key}"
    merriam_dict_list = requests.get(merriam_url).json()
    if (len(merriam_dict_list) == 0):
        return
    if (type(merriam_dict_list[0]) == str):
        return
    merriam_dict_list_0= merriam_dict_list[0]
    definition=""
    if (merriam_dict_list_0.__contains__('shortdef')):
        definitions=merriam_dict_list_0['shortdef']
        definitions_len=len(definitions)
        for i in range(definitions_len):
            definition+=definitions[i]+"; "
    parts_of_speech=""
    if (merriam_dict_list_0.__contains__('fl')):
        parts_of_speech=merriam_dict_list_0['fl']

    audioname=""
    audiourl=""
    if (merriam_dict_list_0.__contains__('hwi')):
        hwi = merriam_dict_list_0['hwi']
        if (hwi.__contains__('prs')):
            prs = hwi['prs']
            prs_len = len(prs)
            for i in range(prs_len):
                if (prs[i].__contains__('sound')):
                    sound = hwi['prs'][i]["sound"]
                    audioname = sound["audio"]
    if(len(audioname)!=0):
        if (audioname[0:2] == "bix"):
            subdir = "bix"
        elif (audioname[0:1] == "gg"):
            subdir = "gg"
        elif (audioname[0].isdigit() or audioname[0] in punctuation):
            subdir = "number"
        else:
            subdir = audioname[0]
        audiourl=f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{audioname}.mp3"


    synonyms=synoList(word)
    antonyms = antoList(word)
    oneExample=giveOneExample(word)
    head = "<b>" + word[0].upper() + word[1:] + "</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + head+", "+parts_of_speech+ "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + definition +"\n\n" + u"\U0001F4DA <b>Example</b> :\n" + oneExample+ "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonyms+ "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n" + antonyms
    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
    if (len(audiourl) != 0):
        update.message.reply_audio(audiourl, caption=f"Pronunciation of {head}",
                                   parse_mode=telegram.ParseMode.HTML)


def search(update, context):
    if update.message.chat.id not in admins:
        ans = "To be used in the group Lingua Franca English House (<a href='https://t.me/+xeg0uDpOFfE4MTJl'>t.me/+xeg0uDpOFfE4MTJl </a>). Join the group if you haven't already thanks 😊😊."
        update.message.reply_text(ans, parse_mode=telegram.ParseMode.HTML)
        return
    msg = f"{update.message.text}"
    word = msg[8:].lower()
    if (word == "lingua franca"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "a language used for communication between groups of people who speak different languages" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "The international business community sees English as a lingua franca." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "meghna"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "Thunder; Also used to refer the holy river Goddess Ganga; One of the best singers" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Thuder, Lightning, Ganges, Holy, Pretty, Beautiful, Melodious, Buddy:), Awesome, Fantastic, Endearing, Best Singer, Best Buddy,"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word== "jo"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "A sweetheart; Beloved one; Dear(often used in addressing a person)" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "I thought it might have been one of the servant girls with her jo.\n Oh you're a jo, she said, when I brought her breakfast in bed." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\nSweetheart"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "rishi"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "A holy Hindu sage; Saint, Inspired poet" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Rishi, IRun Man, Deep Learning, Dark Warrior, Artist, Developer, Engineer"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    merriam_url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={merriam_dict_key}"
    merriam_dict_list = requests.get(merriam_url).json()
    if (len(merriam_dict_list) == 0):
        update.message.reply_text("Sorry! The word was not found in our Dictionary. You can try using the explain function :)")
        return
    if (type(merriam_dict_list[0]) == str):
        update.message.reply_text("Sorry! The word was not found in our Dictionary. You can try using the explain function :)")
        return
    merriam_dict_list_0 = merriam_dict_list[0]
    definition = ""
    if (merriam_dict_list_0.__contains__('shortdef')):
        definitions = merriam_dict_list_0['shortdef']
        definitions_len = len(definitions)
        for i in range(definitions_len):
            definition += definitions[i] + "; "
    parts_of_speech = ""
    if (merriam_dict_list_0.__contains__('fl')):
        parts_of_speech = merriam_dict_list_0['fl']

    audioname = ""
    audiourl = ""
    if (merriam_dict_list_0.__contains__('hwi')):
        hwi = merriam_dict_list_0['hwi']
        if (hwi.__contains__('prs')):
            prs = hwi['prs']
            prs_len = len(prs)
            for i in range(prs_len):
                if (prs[i].__contains__('sound')):
                    sound = hwi['prs'][i]["sound"]
                    audioname = sound["audio"]
    if (len(audioname) != 0):
        if (audioname[0:2] == "bix"):
            subdir = "bix"
        elif (audioname[0:1] == "gg"):
            subdir = "gg"
        elif (audioname[0].isdigit() or audioname[0] in punctuation):
            subdir = "number"
        else:
            subdir = audioname[0]
        audiourl = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{audioname}.mp3"

    # UPDATE THE COUNT ::::::::----->>>
    initial_count = myfile.x
    final_count = initial_count + 2
    myfile.x = final_count

    synonyms = synoList(word)
    antonyms = antoList(word)
    oneExample = giveOneExample(word)
    head = "<b>" + word[0].upper() + word[1:] + "</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + head + ", " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + definition + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + oneExample + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonyms + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n" + antonyms
    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
    if (len(audiourl) != 0):
        update.message.reply_audio(audiourl, caption=f"Pronunciation of {head}",
                                   parse_mode=telegram.ParseMode.HTML)
def find(update, context):
    if update.message.chat.id not in admins:
        ans = "To be used in the group Lingua Franca English House (<a href='https://t.me/+xeg0uDpOFfE4MTJl'>t.me/+xeg0uDpOFfE4MTJl </a>). Join the group if you haven't already thanks 😊😊."
        update.message.reply_text(ans, parse_mode=telegram.ParseMode.HTML)
        return

    msg = f"{update.message.text}"
    word=msg[6:].lower()
    if (word == "lingua franca"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "a language used for communication between groups of people who speak different languages" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "The international business community sees English as a lingua franca." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "meghna"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "Thunder; Also used to refer the holy river Goddess Ganga; One of the best singers" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Thuder, Lightning, Ganges, Holy, Pretty, Beautiful, Melodious, Buddy:), Awesome, Fantastic, Endearing, Best Singer, Best Buddy,"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "jo"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "A sweetheart; Beloved one; Dear(often used in addressing a person)" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "I thought it might have been one of the servant girls with her jo.\n Oh you're a jo, she said, when I brought her breakfast in bed." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\nSweetheart"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "rishi"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "A holy Hindu sage; Saint, Inspired poet" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Rishi, IRun Man, Deep Learning, Dark Warrior, Artist, Developer, Engineer"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return

    head = "<b>" + word[0].upper() + word[1:] + "</b>"


    merriam_url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={merriam_dict_key}"
    merriam_dict_list = requests.get(merriam_url).json()
    if (len(merriam_dict_list) == 0):
        update.message.reply_text("Sorry! The word was not found in our Dictionary. You can try using the explain function :)")
        return
    if (type(merriam_dict_list[0]) == str):
        update.message.reply_text("Sorry! The word was not found in our Dictionary. You can try using the explain function :)")
        return
    merriam_dict_list_0= merriam_dict_list[0]
    definition=""
    if (merriam_dict_list_0.__contains__('shortdef')):
        definitions=merriam_dict_list_0['shortdef']
        definitions_len=len(definitions)
        for i in range(definitions_len):
            definition+=definitions[i]+"; "
    parts_of_speech=""
    if (merriam_dict_list_0.__contains__('fl')):
        parts_of_speech=merriam_dict_list_0['fl']

    audioname=""
    audiourl=""
    if (merriam_dict_list_0.__contains__('hwi')):
        hwi=merriam_dict_list_0['hwi']
        if (hwi.__contains__('prs')):
            prs=hwi['prs']
            prs_len=len(prs)
            for i in range(prs_len):
                if(prs[i].__contains__('sound')):
                    sound=hwi['prs'][i]["sound"]
                    audioname = sound["audio"]
    if(len(audioname)!=0):
        if (audioname[0:2] == "bix"):
            subdir = "bix"
        elif (audioname[0:1] == "gg"):
            subdir = "gg"
        elif (audioname[0].isdigit() or audioname[0] in punctuation):
            subdir = "number"
        else:
            subdir = audioname[0]
        audiourl=f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{audioname}.mp3"

    # UPDATE THE COUNT ::::::::----->>>
    initial_count = myfile.x
    final_count = initial_count + 2
    myfile.x = final_count


    synonyms=synoList(word)
    antonyms = antoList(word)
    oneExample=giveOneExample(word)
    head = "<b>" + word[0].upper() + word[1:] + "</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + head+", "+parts_of_speech+ "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + definition +"\n\n" + u"\U0001F4DA <b>Example</b> :\n" + oneExample+ "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonyms+ "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n" + antonyms
    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
    if(len(audiourl)!=0):
        update.message.reply_audio(audiourl, caption=f"Pronunciation of {head}",
                               parse_mode=telegram.ParseMode.HTML)

def explain(update, context):
    if update.message.chat.id not in admins:
        ans = "To be used in the group Lingua Franca English House (<a href='https://t.me/+xeg0uDpOFfE4MTJl'>t.me/+xeg0uDpOFfE4MTJl </a>). Join the group if you haven't already thanks 😊😊."
        update.message.reply_text(ans, parse_mode=telegram.ParseMode.HTML)
        return
    msg = f"{update.message.text}".lower()
    language = 'en-gb'
    word_id = msg[9:]
    if (word_id == "lingua franca"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper()+word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n"+ "a language used for communication between groups of people who speak different languages" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "The international business community sees English as a lingua franca."+ "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word_id == "meghna"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper()+word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n"+ "Thunder; Also used to refer the holy river Goddess Ganga; One of the best singers" +  "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" +"Thuder, Lightning, Ganges, Holy, Pretty, Beautiful, Melodious, Buddy:), Awesome, Fantastic, Endearing, Best Singer, Best Buddy,"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word_id == "jo"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper() + word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "A sweetheart; Beloved one; Dear(often used in addressing a person)" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "I thought it might have been one of the servant girls with her jo.\n Oh you're a jo, she said, when I brought her breakfast in bed." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\nSweetheart"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word_id == "rishi"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word_id[0].upper()+word_id[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n"+ "A holy Hindu sage; Saint, Inspired poet" +  "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" +"Rishi, IRun Man, Deep Learning, Dark Warrior, Artist, Developer, Engineer"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return

    # UPDATE THE COUNT ::::::::----->>>
    initial_count = myfile.x
    final_count = initial_count + 3
    myfile.x = final_count

    find2(update, context)
    strictMatch = 'false'
    test = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{word_id}?strictMatch=false"
    r = requests.get(test, headers={'app_id': app_id, 'app_key': app_key})
    # print(r.status_code)
    if (r.status_code !=200 ):
        return
    testr = r.json()
    le = testr['results'][0]['lexicalEntries']
    for i in range(len(le)):  # i is representing the number of the lexical entry
        le_i = le[i]
        pos = le_i['lexicalCategory']['text']
        entries = le_i['entries']
        senses = entries[0]['senses']
        for j in range(len(senses)):
            sense_j = senses[j]

            definition = ""
            if (sense_j.__contains__('definitions')):
                definitions = sense_j['definitions']
                for k in range(len(definitions)):
                    definition += definitions[k] + "; "

            example = ""
            if (sense_j.__contains__('examples')):
                examples = sense_j['examples']
                for k in range(len(examples)):
                    example += str(k + 1) + ". "
                    example += examples[k]['text'][0].upper()+examples[k]['text'][1:].lower() + "\n"

            synonym = ""
            if (sense_j.__contains__('synonyms')):
                synonyms = sense_j['synonyms']
                for k in range(len(synonyms)):
                    synonym += synonyms[k]['text'] + "; "

            word = "<b>" + msg[9].upper() + msg[10:].lower() + "</b>"
            strng = u"\U0001F1EE\U0001F1F3" + " " + word + " ," + pos + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + definition + "\n\n" + u"\U0001F4DA <b>Examples</b> :\n" + example + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonym
            update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)

def find2(update, context):
    msg = f"{update.message.text}"
    word=msg[9:].lower()
    merriam_url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={merriam_dict_key}"
    merriam_dict_list = requests.get(merriam_url).json()
    if (len(merriam_dict_list) == 0):
        return
    if (type(merriam_dict_list[0]) == str):
        return
    merriam_dict_list_0= merriam_dict_list[0]
    definition=""
    if (merriam_dict_list_0.__contains__('shortdef')):
        definitions=merriam_dict_list_0['shortdef']
        definitions_len=len(definitions)
        for i in range(definitions_len):
            definition+=definitions[i]+"; "
    parts_of_speech=""
    if (merriam_dict_list_0.__contains__('fl')):
        parts_of_speech=merriam_dict_list_0['fl']

    audioname=""
    audiourl=""
    if (merriam_dict_list_0.__contains__('hwi')):
        hwi = merriam_dict_list_0['hwi']
        if (hwi.__contains__('prs')):
            prs = hwi['prs']
            prs_len = len(prs)
            for i in range(prs_len):
                if (prs[i].__contains__('sound')):
                    sound = hwi['prs'][i]["sound"]
                    audioname = sound["audio"]
    if(len(audioname)!=0):
        if (audioname[0:2] == "bix"):
            subdir = "bix"
        elif (audioname[0:1] == "gg"):
            subdir = "gg"
        elif (audioname[0].isdigit() or audioname[0] in punctuation):
            subdir = "number"
        else:
            subdir = audioname[0]
        audiourl=f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{audioname}.mp3"


    synonyms=synoList(word)
    antonyms = antoList(word)
    oneExample=giveOneExample(word)
    head = "<b>" + word[0].upper() + word[1:] + "</b>"
    strng = u"\U0001F1EE\U0001F1F3" + " " + head+", "+parts_of_speech+ "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + definition +"\n\n" + u"\U0001F4DA <b>Example</b> :\n" + oneExample+ "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + synonyms+ "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n" + antonyms
    update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
    if (len(audiourl) != 0):
        update.message.reply_audio(audiourl, caption=f"Pronunciation of {head}",
                                   parse_mode=telegram.ParseMode.HTML)
def anto(update, context):
    if update.message.chat.id not in admins:
        ans = "To be used in the group Lingua Franca English House (<a href='https://t.me/+xeg0uDpOFfE4MTJl'>t.me/+xeg0uDpOFfE4MTJl </a>). Join the group if you haven't already thanks 😊😊."
        update.message.reply_text(ans, parse_mode=telegram.ParseMode.HTML)
        return
    msg = f"{update.message.text}"
    word = msg[6:]
    if (word == "lingua franca"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "a language used for communication between groups of people who speak different languages" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "The international business community sees English as a lingua franca." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "meghna"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "Thunder; Also used to refer the holy river Goddess Ganga; One of the best singers" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Thuder, Lightning, Ganges, Holy, Pretty, Beautiful, Melodious, Buddy:), Awesome, Fantastic, Endearing, Best Singer, Best Buddy,"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "jo"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "A sweetheart; Beloved one; Dear(often used in addressing a person)" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "I thought it might have been one of the servant girls with her jo.\n Oh you're a jo, she said, when I brought her breakfast in bed." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\nSweetheart"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "rishi"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "A holy Hindu sage; Saint, Inspired poet" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Rishi, IRun Man, Deep Learning, Dark Warrior, Artist, Developer, Engineer"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
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
    if update.message.chat.id not in admins:
        ans = "To be used in the group Lingua Franca English House (<a href='https://t.me/+xeg0uDpOFfE4MTJl'>t.me/+xeg0uDpOFfE4MTJl </a>). Join the group if you haven't already thanks 😊😊."
        update.message.reply_text(ans, parse_mode=telegram.ParseMode.HTML)
        return
    msg = f"{update.message.text}"
    word = msg[6:]
    if (word == "lingua franca"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "a language used for communication between groups of people who speak different languages" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "The international business community sees English as a lingua franca." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\n" + "\n\n" + u"\U0001F4DA <b>Antonyms</b> :\n"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "meghna"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "Thunder; Also used to refer the holy river Goddess Ganga; One of the best singers" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Thuder, Lightning, Ganges, Holy, Pretty, Beautiful, Melodious, Buddy:), Awesome, Fantastic, Endearing, Best Singer, Best Buddy,"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "jo"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\U0001F4DA <b>Definition</b> :\n" + "A sweetheart; Beloved one; Dear(often used in addressing a person)" + "\n\n" + u"\U0001F4DA <b>Example</b> :\n" + "I thought it might have been one of the servant girls with her jo.\n Oh you're a jo, she said, when I brought her breakfast in bed." + "\n\n" + u"\U0001F4DA <b>Synonyms</b> :\nSweetheart"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    elif (word == "rishi"):
        strng = u"\U0001F1EE\U0001F1F3" + " <b>" + word[0].upper() + word[1:] + "</b>, " + "noun" + "\n\n" + u"\u2764\uFE0F <b>Definition</b> :\n" + "A holy Hindu sage; Saint, Inspired poet" + "\n\n" + u"\u2764\uFE0F<b>Synonyms</b> :\n" + "Rishi, IRun Man, Deep Learning, Dark Warrior, Artist, Developer, Engineer"
        update.message.reply_text(strng, parse_mode=telegram.ParseMode.HTML)
        return
    # UPDATE THE COUNT ::::::::----->>>
    initial_count = myfile.x
    final_count = initial_count + 1
    myfile.x = final_count

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
        return example[0].upper()+example[1:]
    return ""

def getCount(update,context):
    count=myfile.x
    update.message.reply_text(count)

#def details(update, context):
 #   context.bot.send_message(update.message.chat.id, str(update))


#def mimic(update, context):
  #  context.bot.send_message(update.message.chat.id, update.message.text)


def error(update, context):
    context.bot.send_message(update.message.chat.id, "OOps! Error encountered")


def main():
    updater = Updater(token=TOKEN)  # updater
    dp = updater.dispatcher  # dispatcher

    ###################   Handlers :
    dp.add_handler(CommandHandler("start", start,filters=Filters._ChatType.private))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("anto", anto))
    dp.add_handler(CommandHandler("syno", syno))
    dp.add_handler(CommandHandler("find", find))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("look", find))
    dp.add_handler(CommandHandler("explain", explain))
    dp.add_handler(CommandHandler("findall", explain))
    dp.add_handler(CommandHandler("lookall", explain))
    dp.add_handler(CommandHandler("searchall", searchall))
    dp.add_handler(CommandHandler("getCount", getCount))

    #dp.add_handler(CommandHandler("details", details))

    #dp.add_handler(MessageHandler(Filters.text, mimic))

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