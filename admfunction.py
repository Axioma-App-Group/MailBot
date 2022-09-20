import telebot
from datetime import date
from config import *
from hideconfig import tok
import os
import time
bot = telebot.TeleBot(tok)

def answerstart(message):
    if message.from_user.id in moderID:
        id = bot.reply_to(message, f"Хорошо, скопируйте id из заявки и отправьте следующим сообщением")
        bot.register_next_step_handler(id, answertext)
    else:
        bot.reply_to(message, f"Ты походу не админ как бы")
def answertext(message):
    data.add({'tgid': message.text})
    text = bot.reply_to(message, f"Теперь введите текст для отправки сообщения")
    bot.register_next_step_handler(text, answersend)
def answersend(message):
    data.add({'message': message.text})
    bot.reply_to(message, f"Сообщение отправлено")
    userid = data.data['tgid']
    msg = data.data['message']
    bot.send_message(userid, f'Сообщение от администратора: \n \n {msg}')

def admcheck(message):
    if message.from_user.id in moderID:
        checkstart(message)
    else:
        bot.reply_to(message, f"Ты походу не админ как бы")
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Получить логи", callback_data="logs"))
    return markup
def checkstart(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    bot.send_message(adminID, f'На данный момент ({today}, {current_time}) бот работает', reply_markup=gen_markup())
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "logs":
        logfile = open(path, 'a')
        print('[LOG] Отправка лога...', file=logfile)
        logfile = open(path, 'r')
        ti_m = os.path.getmtime(path)
        bot.send_document(adminID, logfile, visible_file_name=f'LOG-{time.ctime(ti_m)}.txt',caption=f'Лог от {time.ctime(ti_m)}')
        logfile.close()