import http

import telebot
from time import sleep
import sqlite3
from seleniumwire import webdriver
bot = telebot.TeleBot('')

# Создаем файл с БД
conn = sqlite3.connect('list_users.db')

# Создаем курсор который будет делать запросы в БД
cur = conn.cursor()

# Создаем таблицу в БД 5 колонок
# 1.юзер_id - id в телеграмме
# 2.first name в тг
# 3.last name в тг
# 4.username в дуолинго
# 5.очки при регистрации 2000 (меняется кажд понедельник)
# 6.очки на сайте        2001
# 7.очки в игре          1

# Мак - добавить колонки, как выводит
# Настя -
# Alex - return(bool=True/False, total)

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INT PRIMARY KEY,
   first_name TEXT,
   last_name TEXT,
   user_name TEXT,
   experience_points_start INTEGER,
   experience_points_site INTEGER,
   experience_points_game INTEGER);
""")
conn.commit()
conn.close()

# Добавляем пользователя (образец)
# user = ('00002', 'Raduga', 'Prank You', 'Raduga_prankyou', '300000', '300000', '0')
# cur.execute("""INSERT INTO users(userid, fname, lname, gender)
#    VALUES('00001', 'Alex', 'Smith', 'male');""")
# conn.commit()
# conn.close()


# Добавляем пользователя в формате кортежа
def add_user(a, b, c, d, e, f, g):
    """

    @param a: INT 1.юзер_id - id в телеграмме
    @param b: TEXT 2.first name в тг
    @param c: TEXT 3.last name в тг
    @param d: TEXT 4.username в дуолинго
    @param e: INTEGER 5.очки при регистрации 2000 (меняется кажд понедельник)
    @param f: INTEGER 6.очки на сайте        2001
    @param g: INTEGER 7.очки в игре          1
    """
    user = (a, b, c, d, e, f, g)
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user)
    conn.commit()
    conn.close()


# Обновляем данные пользователя в формате кортежа (юзер, очки на сайте, очки в игре)
def add_data_user(user, a, b):
    cur.execute("UPDATE FROM users SET experience_points_site = a WHERE name=user;")
    conn.commit()
    conn.close()

# Удаляем пользователя по имени
def del_user(user):
    cur.execute("DELETE FROM users WHERE name=user;")
    conn.commit()
    conn.close()


# Берем данные из таблицы
# запрос данных для одного чел
def result_one(user):
    cur.execute("SELECT * FROM users;")
    one_result = cur.fetchone()
    return(one_result)


# запрос данных для первых десяти чел
def result_ten():
    cur.execute("SELECT * FROM users;")
    ten_results = cur.fetchmany(10)
    print(ten_results)


# запрос данных обо всех участниках
def result_all():
    cur.execute("SELECT * FROM users;")
    all_results = cur.fetchall()
    print(all_results)


driver = webdriver.Chrome()
url = 'https://en.duolingo.com/profile/'


def parser(base_url, name):
    """
    This function takes base_url and name user
    returns Total XP of user
    :param base_url:
    :param name:
    :return: bool, Total XP
    """
    full_url = f"{base_url}{name}"
    driver.get(full_url)
    if driver.requests[0].response.status_code == http.HTTPStatus.OK:
        main_page = driver.page_source
        divs = main_page.split(">")
        for i in range(len(divs)):
            if "Total XP" in divs[i]:
                temp_str = divs[i-2]
                total = int(temp_str[:temp_str.find("<"):])
                print(f'{name}: {total}')
                return True, total
    else:
        print(f'Error: {name}')
        return False, 0


@bot.message_handler(commands=['start'])
def reply_to_start(message):
    """ Выводит список команд при отправлении команды старт """
    
    commands_dict = {'/start': "Выводит этот список",
                     "/take_part": "Заносит пользователя в таблицу участников",
                     "/show": "Показывает опыт участников",
                     "/clean": "Очищает таблицу участников",
                     "/show_the_winner": "Показывает победителя и крутую картинку для него",
                     "/help": "Выводит информацию о боте"
                     }
    new_line = '\n'
    bot.send_message(message.chat.id, f'''{new_line.join(f"{key} : {value}" for key, value in commands_dict.items())}''')                     


@bot.message_handler(commands=['take_part'])
def reply_to_take_part(message):
    # Заносим информацию об участнике в БД.
    bot.reply_to(message, "Отлично! Теперь ты участник соревнования. Разгроми соперников!")
    
  
@bot.message_handler(commands=['show'])
def show_table(message):
    """ Показывает результаты количество опыта у участников на данный момент. """
    bot.send_message(message.chat.id, "Таблица участников")   # Скорее всего, понадобятся f-строки или к-либо функция.

    
@bot.message_handler(commands=['clean'])
def clean_bd(message):
    """ Очищает БД после завершения соревнования. """
    bot.send_message(message.chat.id, "БД чиста, как слеза младенца:D")


@bot.message_handler(commands=['show_the_winner'])
def show_the_winner(message):
    """ Выводит имя победителя и картинку для него. """
    pass
                     

@bot.message_handler(commands=['help'])
def help(message):
    """Выводит информацию о боте в ответ на команду /help. """
    bot.send_message(message.chat.id, "Информация о боте")
    

while True: 
        try:
            bot.polling(none_stop=True) 
        except Exception as _ex:
            sleep(15)