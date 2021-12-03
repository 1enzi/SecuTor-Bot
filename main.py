import telebot
from telebot import types
import config
import strings

bot = telebot.TeleBot(config.TESTTOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    menu1 = types.InlineKeyboardButton(strings.test, callback_data='primaryTest')
    menu2 = types.InlineKeyboardButton(strings.regTraining, callback_data='training')
    menu3 = types.InlineKeyboardButton(strings.begin, callback_data='startEducation')

    markup.add(menu1, menu2, menu3)

    bot.send_message(message.chat.id, strings.greetings, reply_markup=markup)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, strings.helpString)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.chat.id, strings.unsignedMessage)


bot.polling(none_stop=True, interval=0)
