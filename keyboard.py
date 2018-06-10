#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from extended_calc import *

BASKET = {}


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
    chat_id = query.message.chat_id

    if query.data is not '=':
        BASKET[chat_id] = BASKET.get(chat_id, '') + query.data
    else:
        bot.edit_message_text(text=calculator(BASKET[chat_id]),chat_id=chat_id,
                          message_id=query.message.message_id)
        del BASKET[chat_id]

