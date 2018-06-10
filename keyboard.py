#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import bot_key

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
PROXY = bot_key.proxy


def start(bot, update):
    keyboard = [[InlineKeyboardButton("1", callback_data='1'),
                 InlineKeyboardButton("2", callback_data='2'),
                 InlineKeyboardButton("3", callback_data='3'),
                 InlineKeyboardButton("+", callback_data='+')],

                [InlineKeyboardButton("4", callback_data='4'),
                 InlineKeyboardButton("5", callback_data='5'),
                 InlineKeyboardButton("6", callback_data='6'),
                 InlineKeyboardButton("-", callback_data='-')],

                [InlineKeyboardButton("7", callback_data='7'),
                 InlineKeyboardButton("8", callback_data='8'),
                 InlineKeyboardButton("9", callback_data='9'),
                 InlineKeyboardButton("*", callback_data='*')],

                [InlineKeyboardButton("0", callback_data='0'),
                 InlineKeyboardButton("/", callback_data='/'),
                 InlineKeyboardButton("=", callback_data='=')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="{}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    # return query.data

    
def sum_button(bot, update):

    thing = ''
    while button is not '=':
        thing += button(bot, update)
    else:
        bot.edit_message_text(text="Сейчас посчитаем!",chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    # calcul.append(button(bot, update))
    print(thing)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_key.key_ring, request_kwargs=PROXY)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()