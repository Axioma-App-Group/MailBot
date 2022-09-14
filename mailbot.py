import telebot
import openpyxl
import csv
import time
import secrets
import string
from datetime import date
from transliterate import translit
from config import tok
from config import adminID
import os
log = open('LOG.txt', 'r')
bot = telebot.TeleBot(tok)

os.system("cls")
print("[LOG] Бот Запущен")
class Data(object):
    def __init__(self) -> None:
        self.data:dict={}
        self.i_obj2=0
        self.i_obj1=0
    def add(self,data:dict) -> None:
        self.data.update(data)
    def obj(self,num):
        if num==1:self.i_obj1+=1
        else: self.i_obj2+=1
data:object=Data()

@bot.message_handler(commands=['start'])
def start(message):
    print(f"[LOG] [{message.from_user.username}] [start]")
    print(f"[LOG] [{message.from_user.username}] [start]")
    bot.send_message(message.chat.id, f"""Приветствую, {message.from_user.first_name}. Вы попали к почтовому боту ЧРТ
    Для регистрации почты введите команду /register
    Для восстановления пароля введите команду /recovery
    Для предоставления списка проектов введите /prjlist
    """, parse_mode = "Markdown")

@bot.message_handler(commands=['register'])
def register_name(message):
    print(f"[LOG] [{message.from_user.username}] [register_name]")
    mesg = bot.send_message(message.chat.id, f"Для начала введите своё имя", parse_mode = 'Markdown')
    bot.register_next_step_handler(mesg, register_surname)
def register_surname(message):
     print(f"[LOG] [{message.from_user.username}] [register_surname]")
    mesg = bot.send_message(message.chat.id, f"Теперь введите фамилию")
    en_text = translit(message.text, language_code='ru', reversed=True)
    en_text = en_text.lower()
    ru_text = message.text
    data.add({'name': en_text})
    data.add({'ru_name': ru_text})
    bot.register_next_step_handler(mesg, register_id)
def register_id(message):
    print(f"[LOG] [{message.from_user.username}] [register_id]")
    en_text = translit(message.text, language_code='ru', reversed=True)
    ru_text = message.text
    en_text = en_text.lower()
    data.add({'surname': en_text})
    data.add({'ru_surname': ru_text})
    photo = open("studentid.png", 'rb')
    textmesg = f'Напоследок введите номер студенческого билета'
    mesg = bot.send_photo(message.chat.id, photo, caption = textmesg, parse_mode='Markdown')
    bot.register_next_step_handler(mesg, register_end)
def register_end(message):
    print(f"[LOG] [{message.from_user.username}] [register_end]")
    id = message.text.upper()
    data.add({"id": id})
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    text = f"""
    Я проверил, и вы действительно не имеете почты в доменной зоне radiotech\\.su и являетесь студентом ЧРТ 
    Ваша новая почта  {data.data['name']}\\.{data.data['surname']}@radiotech\\.su  Пароль \\- {password}
    Ваша почта скоро будет активна и вход по ней будет доступен\\!
    """
    chektext = f'*Проверка в базе данных учеников\\.\\.\\.*'
    chekmsg = bot.send_message(message.chat.id, chektext, parse_mode='MarkdownV2')
    time.sleep(5)
    bot.edit_message_text(text, chekmsg.chat.id, chekmsg.message_id, parse_mode='MarkdownV2')
    mail = f"{data.data['name']}.{data.data['surname']}@radiotech.su"
    minimail = f"{data.data['name']}.{data.data['surname']}"
    wb = openpyxl.open("data.xlsx")
    wb.active = 0
    sheet = wb.active
    sheet.append([data.data['id'], mail, password, message.from_user.id, message.from_user.username])
    wb.save("registerdata.xlsx")
    firstname = data.data['ru_name']
    lastname = data.data['ru_surname']
    groups = 'student'
    with open("registerusers.csv", "a", encoding='CP1251') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'password', 'firstname', 'lastname', 'groups'])
        writer.writerow([minimail, password, firstname, lastname, groups])
@bot.message_handler(commands=['recovery'])
def recovery_mail(message):
    print(f"[LOG] [{message.from_user.username}] [recovery_mail]")
    mesg = bot.send_message(message.chat.id, f'Вас понял. Для заявки на восстановление почты введите свой адрес электронной почты вида name.surname@radiotech.su')
    bot.register_next_step_handler(mesg, recovery_idphoto)
def recovery_idphoto(message):
    print(f"[LOG] [{message.from_user.username}] [recovery_idphoto]")
    data.add({"mail": message.text})
    photo = open("studentid.png",'rb')
    textmesg = f'Теперь введите номер студенческого билета, чтобы найти его, посмотрите на фотографию'
    mesg = bot.send_photo(message.chat.id, photo, caption = textmesg, parse_mode='MarkdownV2' )
    bot.register_next_step_handler(mesg, recovery_accepting)
def recovery_accepting(message):
    print(f"[LOG] [{message.from_user.username}] [recovery_accepting]")
    data.add({"id": message.text})
    bot.send_message(message.chat.id, f"Заявка на восстановление пароля передана администрации. Ожидайте")
    mail = data.data['mail']
    id = data.data['id']
    bot.send_message(adminID, f"""
    *Заявка* на восстановление пароля
    *Почта* - {mail}
    *Номер* - {id}
    *TGUN* - @{message.from_user.username}
    *TGID* - {message.from_user.id}
    """, parse_mode='Markdown')

@bot.message_handler(commands=['prjlist'])
def prjlist(message):
    print(f"[LOG] [{message.from_user.username}] [prjlist]")
    today = date.today()
    bot.send_message(message.chat.id, f'''Актуальные на *{today}* проекты:
    [Почтовый ТГ бот](https://t.me/mailcrt_bot)
    ''', parse_mode='Markdown')
@bot.message_handler(commands=['admhelp'])
def helpstart(message):
    print(f"[LOG] [{message.from_user.username}] [helpstart]")
    mesg = bot.send_message(message.chat.id, f'''Вас понял, до призыва на помощь осталось только описать проблему''')
    bot.register_next_step_handler(mesg, helpdescription)
def helpdescription(message):
    print(f"[LOG] [{message.from_user.username}] [helpdescription]")
    data.add({"description": message.text})
    bot.send_message(message.chat.id, f"""Наши администраторы только что получили уведомление от вас. Ожидайте""")
    bot.send_message(adminID, f"""
    Призыв о помощи от {message.from_user.first_name}
    *TGUN* - @{message.from_user.username}
    *TGID* - {message.from_user.id}
    *Описание* - {data.data['description']}
    """, parse_mode = "Markdown")
bot.polling(none_stop=True, interval=0)
try:
    bot.polling(none_stop=True)
except Exception as e:
    logger.exception("Fail startup:", e)
