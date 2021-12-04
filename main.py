import telebot
from pymongo import MongoClient
from telebot import types
import config
import strings

bot = telebot.TeleBot(config.TESTTOKEN)


class User:
    def __init__(self, new_first_name, new_last_name):
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.is_register = False

    @property
    def get_first_name(self):
        return self.first_name

    @property
    def get_last_name(self):
        return self.last_name

    def register_user(self):
        self.is_register = True


class DataBase:
    def __init__(self):
        cluster = MongoClient(strings.clusterURL)

        self.users = cluster["SecuTor"]
        self.collection = self.users["SecuTor"]

        self.User_Count = len(list(self.users.find({})))

    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})

        if user is not None:
            return user

        user = {
            "chat_id": chat_id,
            "task_index": None
        }

        self.users.insert_one(user)

        return user


db = DataBase()
Main_User = User()


@bot.message_handler(commands=['start'])
def start_message(message):
    Main_User.__init__(message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.chat.id, ('Привет, ' + Main_User.get_first_name + '!'))
    bot.send_message(message.chat.id, strings.initialization)
    bot.send_message(message.chat.id, db.get_user())

    if db.collection.find_one({"username": message.from_user.username}) is None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        menu_one = types.InlineKeyboardButton(strings.register, callback_data='register')
        markup.add(menu_one)
        bot.send_message(message.chat.id, strings.userNotFound, reply_markup=markup)

    else:
        bot.send_message(message.chat.id, strings.userFound)


def open_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)

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
    if message == 'Начать обучение':
        bot.send_message(message.chat.id, strings.unsignedMessage)


bot.polling(none_stop=True, interval=0)
