from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
import logging
import bot_key
import random
import ephem
import datetime
from lexicon import *
from extended_calc import *
from full_moon import *
import keyboard


# Настройки прокси
PROXY = bot_key.proxy

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def translation(en_full, en):
    if en_full not in lexicon:
        return en
    else:
        en_ru = 'En: {}, ru: {}'.format(en,lexicon[en_full])
        return en_ru


def find_planet(bot, update, planet):
    pl = getattr(ephem, planet)()
    pl.compute(datetime.datetime.now().strftime('%Y/%m/%d'))

    print(ephem.constellation(pl))

    en = ephem.constellation(pl)
    en_ru = translation(en[1], en)

    update.message.reply_text(en_ru)


def greet_planet(bot, update):
    user_text = update.message.text
    text = 'Вызван /planet'
    update.message.reply_text(text)

    if " " in user_text:
        planet = user_text.split(' ')[1].capitalize()
        find_planet(bot, update, planet)


def bot_answers(bot, update):
	punctuation_mark = ['!', '?', '...', '?!', ' :)', ' :(', ' ^-^', ' $%^#']
	return random.choice(punctuation_mark)


def greet_user(bot, update):
    text = 'Здравствуй, дорогой друг!Что бы узнать, что я могу, набери /help.'
    update.message.reply_text(text)


def calc_keyboard(bot, update):
    # клавиатура
   
    custom_keyboard = [
                        ['1', '2', '3', '+'],
                        ['4', '5', '6', '-'],
                        ['7', '8', '9', '*'],
                        ['/', '0', '=']
                       ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    # query = update.callback_query
    # print(dir(update))

    bot.send_message(chat_id=update.message.chat_id, 
                     text="test", 
                     reply_markup=reply_markup)
    print(bot.send_message.text)


def remove_keyboard(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=update.message.chat_id, text="I'm back.", reply_markup=reply_markup)
    # print(dir(update.message))


def calc(bot, update, user_text):
    text = user_text.strip(' ')

    try:
        # keyboard.start(bot, update)
        calc_keyboard(bot, update)
        # remove_keyboard(bot, update)
        
    except AttributeError as e:
        print(e)
        update.message.reply_text('что-то не получилось')

    c = text[:-1]

    update.message.reply_text(calculator(c))


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    if '=' in user_text:
        print(user_text)
        calc(bot, update, user_text)
    elif 'когда' and 'полнолуние' in user_text.lower():
        update.message.reply_text(moon_full(user_text))
    else:
        update.message.reply_text(user_text + bot_answers(bot, update))


def count_word(bot, update):
    user_text = update.message.text
    print(user_text)
    if '"' in user_text:
        word = user_text.split('"')[1]
        print(word)
        if word:
            result = word.strip()
            # c_word = words.split(' ')
            # print(c_word)
            # print(len(c_word))
            update.message.reply_text(len(result))
        else:
            update.message.reply_text('Тут пустая строка!')

    elif "'" in user_text:
        update.message.reply_text('Слово нужно писать в двойных кавычках.')

    else:
        update.message.reply_text('не было кавычек!')


def help(bot, update):
    update.message.reply_text(
        """
        Use '/start' to say hello this bot.
        Use '/planet planet_name' to would know in which constellation the planet is now.
        Use '/calculate' or 'your example=' to count.(to do).
        Use '/fullmoon your_date(day-month-year)' to find out when the next full moon(to do).
        Use '/wordcount "your_word"' to find the length of a word.
        Use /remove_keyboard to remove keyboard.
        """)


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(bot_key.key_ring, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", greet_planet))
    dp.add_handler(CommandHandler("wordcount", count_word))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    # dp.add_handler(CallbackQueryHandler(keyboard.button))
    # dp.add_handler(CallbackQueryHandler(keyboard.sum_button))
    dp.add_handler(CommandHandler('help', help))

    mybot.start_polling()
    mybot.idle()


main()
