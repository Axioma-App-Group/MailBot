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
from config import path
import os
import time
logfile = open(path, 'a')
print('[LOG] end log', file = logfile)
logfile.close()
logfile = open (path, 'r')
ti_m = os.path.getmtime(path)
bot = telebot.TeleBot(tok)
bot.send_document(adminID, logfile, caption = f'Лог от {time.ctime(ti_m)}')
os.system("cls")
print("[LOG] Бот Запущен")
logfile.close()
os.remove(path)
class IsPrivate(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_private'
    @staticmethod
    def check(message: telebot.types.Message):
        return message.chat.type == "private"
bot.add_custom_filter(IsPrivate())
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

@bot.message_handler(commands=['start'],is_private=True)
def start(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [start]")
    print(f"[LOG] [{message.from_user.username}] [start]", file = file)
    file.close()
    bot.send_message(message.chat.id, f"""Приветствую, {message.from_user.first_name}. Вы попали к почтовому боту ЧРТ
    Для регистрации почты введите команду /register
    Для восстановления пароля введите команду /recovery
    Для предоставления списка проектов введите /prjlist
    """, parse_mode = "Markdown")

@bot.message_handler(commands=['register'],is_private=True)
def register_name(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [register_name]")
    print(f"[LOG] [{message.from_user.username}] [register_name]", file = file)
    file.close()
    mesg = bot.send_message(message.chat.id, f"Для начала введите своё имя", parse_mode = 'Markdown')
    bot.register_next_step_handler(mesg, register_surname)
def register_surname(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [register_surname]")
    print(f"[LOG] [{message.from_user.username}] [register_surname]", file = file)
    file.close()
    mesg = bot.send_message(message.chat.id, f"Теперь введите фамилию")
    en_text = translit(message.text, language_code='ru', reversed=True)
    en_text = en_text.lower()
    ru_text = message.text
    data.add({'name': en_text})
    data.add({'ru_name': ru_text})
    bot.register_next_step_handler(mesg, register_id)
def register_id(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [register_id]")
    print(f"[LOG] [{message.from_user.username}] [register_id]", file = file)
    file.close()
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
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [register_end]")
    print(f"[LOG] [{message.from_user.username}] [register_end]", file = file)
    file.close()
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
@bot.message_handler(commands=['recovery'],is_private=True)
def recovery_mail(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [recovery_mail]")
    print(f"[LOG] [{message.from_user.username}] [recovery_mail]", file=file)
    file.close()
    mesg = bot.send_message(message.chat.id, f'Вас понял. Для заявки на восстановление почты введите свой адрес электронной почты вида name.surname@radiotech.su')
    bot.register_next_step_handler(mesg, recovery_idphoto)
def recovery_idphoto(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [recovery_idphoto]")
    print(f"[LOG] [{message.from_user.username}] [recovery_idphoto]", file = file)
    file.close()
    data.add({"mail": message.text})
    photo = open("studentid.png",'rb')
    textmesg = f'Теперь введите номер студенческого билета, чтобы найти его, посмотрите на фотографию'
    mesg = bot.send_photo(message.chat.id, photo, caption = textmesg, parse_mode='MarkdownV2' )
    bot.register_next_step_handler(mesg, recovery_accepting)
def recovery_accepting(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [recovery_accepting]")
    print(f"[LOG] [{message.from_user.username}] [recovery_accepting]", file = file)
    file.close()
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
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [prjlist]")
    print(f"[LOG] [{message.from_user.username}] [prjlist]", file = file)
    file.close()
    today = date.today()
    bot.send_message(message.chat.id, f'''Актуальные на *{today}* проекты:
    [Почтовый ТГ бот](https://t.me/mailcrt_bot)
    ''', parse_mode='Markdown')
@bot.message_handler(commands=['admhelp'],is_private=True)
def helpstart(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [helpstart]")
    print(f"[LOG] [{message.from_user.username}] [helpstart]", file = file)
    file.close()
    mesg = bot.send_message(message.chat.id, f'''Вас понял, до призыва на помощь осталось только описать проблему''')
    bot.register_next_step_handler(mesg, helpdescription)
def helpdescription(message):
    file = open(path, 'a')
    print(f"[LOG] [{message.from_user.username}] [helpdescription]")
    print(f"[LOG] [{message.from_user.username}] [helpdescription]", file = file)
    file.close()
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
