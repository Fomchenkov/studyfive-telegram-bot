#!/usr/bin/env python3

import telebot
from telebot import types

import util
import config


bot = telebot.TeleBot(config.BOT_TOKEN)
READY_TO_ORDER = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id
    cid = message.chat.id
    markup = types.ReplyKeyboardMarkup(
		one_time_keyboard=False, resize_keyboard=True, row_width=1)
    for x in config.main_manu_buttons:
        markup.add(x)
    return bot.send_message(cid, config.main_text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    return bot.send_message(message.chat.id, config.help_message)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    uid = message.from_user.id
    cid = message.chat.id

    if message.text == '⬅️ Отмена':
        if uid in READY_TO_ORDER:
            del READY_TO_ORDER[uid]
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True, row_width=1)
        for x in config.main_manu_buttons:
            markup.add(x)
        return bot.send_message(cid, config.main_text, reply_markup=markup)

    # Handle order action 
    if uid in READY_TO_ORDER:
        if 'name' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['name'] = message.text
            text = 'Введите email'
            return bot.send_message(cid, text)
        if 'email' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['email'] = message.text
            text = 'Введите номер телефона'
            return bot.send_message(cid, text)
        if 'phone_number' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['phone_number'] = message.text
            text = 'Выберите вид работы'
            markup = types.ReplyKeyboardMarkup(
		        one_time_keyboard=True, resize_keyboard=True, row_width=1)
            for work in config.work_types:
                markup.add(work)
            markup.add('⬅️ Отмена')
            return bot.send_message(cid, text, reply_markup=markup)
        if 'work_type' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['work_type'] = message.text
            text = 'Введите предмет'
            markup = types.ReplyKeyboardMarkup(
		        one_time_keyboard=True, resize_keyboard=True, row_width=1)
            markup.add('⬅️ Отмена')
            return bot.send_message(cid, text, reply_markup=markup)
        if 'subject' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['subject'] = message.text
            text = 'Введите количество страниц'
            return bot.send_message(cid, text)
        if 'page_count' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['page_count'] = message.text
            text = 'Введите тему работы'
            return bot.send_message(cid, text)
        if 'work_topic' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['work_topic'] = message.text
            text = 'Введите срок выполнения'
            return bot.send_message(cid, text)
        if 'work_term' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['work_term'] = message.text
            text = 'Введите дополнительную информацию, если требуется'
            return bot.send_message(cid, text)
        if 'add_info' not in READY_TO_ORDER[uid]:
            READY_TO_ORDER[uid]['add_info'] = message.text
            print(READY_TO_ORDER[uid])
            order = util.WorkOrder(
                READY_TO_ORDER[uid]['name'],
                READY_TO_ORDER[uid]['email'],
                READY_TO_ORDER[uid]['phone_number'],
                READY_TO_ORDER[uid]['work_type'],
                READY_TO_ORDER[uid]['subject'],
                READY_TO_ORDER[uid]['page_count'],
                READY_TO_ORDER[uid]['work_topic'],
                READY_TO_ORDER[uid]['work_term'],
                READY_TO_ORDER[uid]['add_info'],
            )
            del READY_TO_ORDER[uid]
            order_text = util.generate_order_text(order)
            print(order_text)
            email_user = util.EmailUser(config.email_login, config.email_password)
            util.send_email(email_user, config.manager_email, 'Новый заказ', order_text)
            text = 'Ваша заявка оформлена!'
            markup = types.ReplyKeyboardMarkup(
                one_time_keyboard=False, resize_keyboard=True, row_width=1)
            for x in config.main_manu_buttons:
                markup.add(x)
            return bot.send_message(cid, text, reply_markup=markup)

    # Handle main menu buttons
    if message.text in config.main_manu_buttons:
        if message.text == 'Заказать работу':
            text = 'Введите свое имя'
            READY_TO_ORDER[uid] = {}
            markup = types.ReplyKeyboardMarkup(
                one_time_keyboard=False, resize_keyboard=True, row_width=1)
            markup.add('⬅️ Отмена')
            return bot.send_message(cid, text, reply_markup=markup)
        elif message.text == 'Наши услуги':
            for text in config.services:
                bot.send_message(cid, text, parse_mode='markdown')
            return
        elif message.text == 'Гарантии':
            for text in config.assurances:
                bot.send_message(cid, text, parse_mode='markdown')
            return
        elif message.text == 'Контакты':
            return bot.send_message(cid, config.contacts, parse_mode='markdown')
        elif message.text == 'О компании':
            return bot.send_message(cid, config.about_company_text, parse_mode='markdown')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
