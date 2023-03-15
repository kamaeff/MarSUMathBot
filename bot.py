#176.119.147.71
import telebot
import config
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

name = ''
surname = ''
q = 5
i = 0
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Добро пожаловать на тестирование математической грамотности для начала напиши /reg")
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Для начала прохождения теста напиши /reg")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
       
    bot.send_message(message.from_user.id, f'{name} теперь мне нужна твоя фамилия: ');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
        
    print(name, surname)
    
    connect = sqlite3.connect('users.db')
    cursour = connect.cursor()
    cursour.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            fstName TEXT,
            secName TEXT,
            userResault INTEGER 
        )""")
    connect.commit()
    
    nowUser = message.chat.id
    cursour.execute(f"SELECT id FROM users WHERE id={nowUser}")
    data = cursour.fetchone()
    
    if data is None:
        user_id = message.chat.id
        cursour.execute(f"INSERT INTO users VALUES(?,?,?,?)", (user_id, name, surname,i))
        connect.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_yes = types.KeyboardButton(text='✅') #кнопка «Да»  
        key_no = types.KeyboardButton(text='❌')
        keyboard.add(key_yes, key_no)
        
        question = bot.send_message(message.chat.id, f"{surname} {name}, готов(а) ли ты пройти тестирование?", reply_markup=keyboard)
        bot.register_next_step_handler(question, user_answer)
    else:
        nowUser = message.chat.id
        cursour.execute(f"SELECT userResault FROM users WHERE id={nowUser}")
        res = cursour.fetchone()[0]
        msg = bot.send_message(nowUser, f'Ты уже прошел тест! {name} ваш результат был {res} из {q}')
        bot.register_next_step_handler(msg, start)
    
   
    
def user_answer(message):
    if message.text == "✅":
        
        keyboard_ques1 = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
        key_1 = types.KeyboardButton(text='0.5') #кнопка «Да»  
        key_2 = types.KeyboardButton(text='1.5')
        key_3 = types.KeyboardButton(text='2.3')
        key_4 = types.KeyboardButton(text='2.6')
        keyboard_ques1.add(key_1, key_2, key_3, key_4)
        
        p = open('Capture.PNG', 'rb')
        bot.send_photo(message.chat.id, p)
        
        msg = bot.send_message(message.chat.id, "Добро пожаловать на тестирование, вот ваша первая задача:\n"\
            "Чему примерно равно расстояние от линии старта до начала самого длинного прямого"\
                "участка трассы?", reply_markup=keyboard_ques1)
        
        
        bot.register_next_step_handler(msg, ques2)
        
    elif message.text == "❌":
        bot.send_message(message.chat.id, "Пока-пока!")
        
def ques2(message):
    if message.text == "1.5":
        global i
        i+=1
        bot.send_message(message.chat.id, "Правильно! Вот тебе следующая задача:\n")
        
    else:
        bot.send_message(message.chat.id, "Ответ не верный, но не расстраивайся! Вот тебе следующая задача:\n")
        
    keyboard_ques2 = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    key_1 = types.KeyboardButton(text='12') #кнопка «Да»  
    key_2 = types.KeyboardButton(text='14')
    key_3 = types.KeyboardButton(text='16')
    key_4 = types.KeyboardButton(text='20')
    keyboard_ques2.add(key_1, key_2, key_3, key_4)
    
    msg = bot.send_message(message.chat.id,f"В результате глобального потепления некоторые ледники начинают таять."\
        "Спустя двенадцать лет после исчезновения льда, на камнях начинают расти крошечные растения,лишайники.\n"\
            "Взаимосвязь между диаметром данного круга и возрастом лишайника можно представить в"\
                "виде формулы:\n"\
                    "d = 7.0 х √(𝒕 − 𝟏𝟐) для t ≥ 12\n"\
                        "где d - это диаметр лишайника в миллиметрах, а t - количество прошедших лет после исчезновения льда\n"\
                            "Вопрос: \n"\
                                "Используя данную формулу, вычислите диаметр лишайника спустя 16 лет после"\
                                    "исчезновения льда.", reply_markup=keyboard_ques2)

    
    bot.register_next_step_handler(msg, ques3)
        
        
def ques3(message):
    if message.text == "14":
        global i 
        i+=1
        bot.send_message(message.chat.id, "Правильно! Вот тебе следующая задача:\n")
        
    else:
        bot.send_message(message.chat.id, "Ответ не верный, но не расстраивайся! Вот тебе следующая задача:\n")
        
    keyboard_ques3 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    key_1 = types.KeyboardButton(text='10') #кнопка «Да»  
    key_2 = types.KeyboardButton(text='11')
    key_3 = types.KeyboardButton(text='12')
    keyboard_ques3.add(key_1, key_2, key_3)
    
    p2 = open('Capture2.PNG', 'rb')
    bot.send_photo(message.chat.id, p2)
    
    msg = bot.send_message(message.chat.id, "Какое число можно поставить вместо вопросительного знака указаного выше на картинке?\n", reply_markup=keyboard_ques3)
    
    bot.register_next_step_handler(msg, ques4)
    
def ques4(message):
    if message.text == '12':
        global i 
        i+=1
        bot.send_message(message.chat.id, "Правильно! Вот тебе следующая задача:\n")
        
    else:
        bot.send_message(message.chat.id, "Ответ не верный, но не расстраивайся! Вот тебе следующая задача:\n")
        
    keyboard_ques4 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    key_1 = types.KeyboardButton(text='4%') #кнопка «Да»  
    key_2 = types.KeyboardButton(text='4.4%')
    key_3 = types.KeyboardButton(text='4.6%')
    key_4 = types.KeyboardButton(text='4.8%')
    keyboard_ques4.add(key_1, key_2, key_3, key_4)
        
    msg = bot.send_message(message.chat.id, "Самат налил в ведро 4 литра молока трехпроцентной (3%) жирности, а "\
        "Олжас 6 литров молока шестипроцентной (6%) жирности. Сколько процентов"\
            "составляет жирность молока в ведре?", reply_markup=keyboard_ques4)   

    
    bot.register_next_step_handler(msg, ques5)

def ques5(message):
    if message.text == '4.8%':
        global i 
        i+=1
        bot.send_message(message.chat.id, "Правильно! Вот тебе следующая задача:\n")
        
    else:
        bot.send_message(message.chat.id, "Ответ не верный, но не расстраивайся! Вот тебе следующая задача:\n")
        
    
    keyboard_ques5 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    key_1 = types.KeyboardButton(text='85') #кнопка «Да»  
    key_2 = types.KeyboardButton(text='82')
    key_3 = types.KeyboardButton(text='17')
    key_4 = types.KeyboardButton(text='14')
    key_5 = types.KeyboardButton(text='36')
    keyboard_ques5.add(key_1, key_2, key_3, key_4, key_5)
        
    msg = bot.send_message(message.chat.id, "Среднее арифметическое шести чисел равно 70, а среднее других четырех"\
        "чисел равно 100. Все десять чисел сложили. Чему равно их среднее"\
            "арифметическое?", reply_markup=keyboard_ques5)  
     
    bot.register_next_step_handler(msg, resault)

def resault(message):
    if message.text == "82":
        global i
        i+=1
        bot.send_message(message.chat.id, "Правильно! Подведем итоги!\n")   
    else:
        bot.send_message(message.chat.id, "Ответ не верный, но не расстраивайся! Подведем итоги\n")
    
    keyboard_resault = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    key_1 = types.KeyboardButton(text='Посмотреть результаты') 
    key_2 = types.KeyboardButton(text='Закончить тестирование')
    keyboard_resault.add(key_1,key_2)
    
    msg = bot.send_message(message.chat.id, f"{name} ты прошел(а) тест, а тепреь выбри действие!", reply_markup=keyboard_resault)
    
    bot.register_next_step_handler(msg, end_test)


def end_test(message):
    global i
    global q
    if message.text == "Посмотреть результаты":
        if i>=3:
            msg = bot.send_message(message.chat.id, f'{name} вы прошли тест успешно! Решено {i} из {q} вопросов. Удачи!\n')
            bot.register_next_step_handler(msg, start)
        elif i<3:            
            msg = bot.send_message(message.chat.id, f"{name} вы не прошли тест! Решено {i} из {q} вопросов!")
            
            bot.register_next_step_handler(msg, start)
        
        connect = sqlite3.connect('users.db')
        cursour = connect.cursor()
        user_id = message.chat.id
        cursour.execute(f"UPDATE users SET userResault = '{i}' WHERE id = '{user_id}'")
        connect.commit()
        
        connect.close()
        
        i=0
    
    elif message.text == "Закончить тестирование":
        msg = bot.send_message(message.chat.id, f'{name}, удачи!')
        bot.register_next_step_handler(msg, start)
        i=0

    

bot.polling(none_stop=True, interval=0)