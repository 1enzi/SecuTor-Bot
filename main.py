import telebot
import pymongo
from pymongo import MongoClient
from telebot import types
import config
import strings

bot = telebot.TeleBot(config.TESTTOKEN)


class DataBase:
    def __init__(self):
        cluster = MongoClient(strings.clusterURL)

        self.db = cluster["SecuTor"]
        self.users = self.db["SecuTor"]

    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})

        if user is not None:
            return user

        else:
            user = {
                "chat_id": chat_id,
                "task_index": None
            }

            self.users.insert_one(user)

            return user


db = DataBase()


@bot.message_handler(commands=['start'])
def start_message(message):
    user = db.get_user(message.chat.id)

    bot.send_message(message.chat.id, ('Привет, ' + main_user.get_first_name + '!'))
    bot.send_message(message.chat.id, strings.initialization)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_one = types.KeyboardButton(strings.start_message)
    markup.add(menu_one)
    bot.send_message(user["chat_id"], strings.userFound, reply_markup=markup)


def open_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    menu_one = types.InlineKeyboardButton(strings.test, callback_data='primaryTest')
    menu_two = types.InlineKeyboardButton(strings.regTraining, callback_data='training')
    menu_three = types.InlineKeyboardButton(strings.begin, callback_data='startEducation')

    markup.add(menu_one, menu_two, menu_three)

    bot.send_message(message.chat.id, strings.greetings, reply_markup=markup)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, strings.helpString)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message == strings.start_message:
        open_main_menu(message)
    else:
        bot.send_message(message.chat.id, strings.unsignedMessage)


bot.polling(none_stop=True, interval=0)
