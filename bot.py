from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import bot_key
import random
import ephem
import datetime
from lexicon import *
from extended_calc import *
from full_moon import *


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
    # now = datetime.datetime.now().strftime('%Y/%m/%d')
    pl = getattr(ephem, planet)()
    pl.compute(datetime.datetime.now().strftime('%Y/%m/%d'))

    print(ephem.constellation(pl))

    en = ephem.constellation(pl)
    en_ru = translation(en[1], en)

    update.message.reply_text(en_ru)


def greet_planet(bot, update):
    user_text = update.message.text
    text = 'Вызван /planet'
    print(text)
    update.message.reply_text(text)

    if " " in user_text:
        planet = user_text.split(' ')[1].capitalize()
        print(planet)

        find_planet(bot, update, planet)


def bot_answers(bot, update):
	punctuation_mark = ['!', '?', '...', '?!', ' :)', ' :(', ' ^-^', ' $%^#']
	return random.choice(punctuation_mark)


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def calc(bot, update, user_text):
    text = user_text.strip(' ')
    if '=' in text:
        # клавиатура
        # custom_keyboard = [
        #                     ['top-left', 'top-right'], 
        #                     ['bottom-left', 'bottom-right']
        #                    ]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        # bot.send_message(chat_id=chat_id, 
        #              text="Custom Keyboard Test", 
        #              reply_markup=reply_markup)

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
        words = user_text.split('"')[1]
        print(words)
        if words:
            c_word = words.split(' ')
            print(c_word)
            print(len(c_word))
            update.message.reply_text(len(c_word))
        else:
            print('Тут пустая строка!')
            update.message.reply_text('Тут пустая строка!')

    elif "'" in user_text:
        print('Слово нужно писать в двойных кавычках.')
        update.message.reply_text('Слово нужно писать в двойных кавычках.')

    else:
        print('не было кавычек!')
        update.message.reply_text('не было кавычек!')


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(bot_key.key_ring, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", greet_planet))
    dp.add_handler(CommandHandler("wordcount", count_word))

    mybot.start_polling()
    mybot.idle()


main()
