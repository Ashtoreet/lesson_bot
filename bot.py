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


def remove_keyboard(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=update.message.chat_id, text="I'm back.", reply_markup=reply_markup)


def calc(bot, update):
    # text = user_text.strip(' ')

    try:
        keyboard.start(bot, update)
        
    except AttributeError as e:
        print(e)
        update.message.reply_text('что-то не получилось')

    # c = text[:-1]

    # update.message.reply_text(calculator(c))


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    if '=' in user_text:
        print(user_text)
        calc(bot, update)
    elif 'когда' and 'полнолуние' in user_text.lower():
        update.message.reply_text(moon_full(user_text))
    else:
        update.message.reply_text(user_text + bot_answers(bot, update))


def help(bot, update):
    update.message.reply_text(
        """
        Use '/start' to say hello this bot.
        Use '/planet planet_name' to would know in which constellation the planet is now.
        Use '/calculate' or '=' to count.(to do).
        Use '/fullmoon your_date(day-month-year)' to find out when the next full moon(to do).
        Use /remove_keyboard to remove keyboard.
        """)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(bot_key.key_ring, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", greet_planet))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))

    dp.add_handler(CommandHandler("calculate", calc))
    
    dp.add_handler(CallbackQueryHandler(keyboard.button))
    dp.add_handler(CommandHandler('help', help))
    dp.add_error_handler(error)


    mybot.start_polling()
    mybot.idle()


main()
