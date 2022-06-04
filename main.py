import http
import random
import telebot
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from conf import xxx

bot = telebot.TeleBot(xxx)

# Создаем файл с БД
conn = sqlite3.connect("list_users.db", check_same_thread=True)

# Создаем курсор который будет делать запросы в БД
curs = conn.cursor()

# Создаем таблицу в БД 7 колонок
# 1.юзер_id - id в телеграмме
# 2.first name в тг
# 3.last name в тг
# 4.username в дуолинго
# 5.очки при регистрации 2000 (меняется кажд понедельник)
# 6.очки на сайте        2001
# 7.очки в игре          1

curs.execute(
    """CREATE TABLE IF NOT EXISTS users(
   user_id INT PRIMARY KEY,
   first_name TEXT,
   last_name TEXT,
   user_name TEXT,
   experience_points_start INTEGER,
   experience_points_site INTEGER,
   experience_points_game INTEGER);
"""
)
conn.commit()
curs.close()


def add_user(a, b, c, d, e, f, g):
    """
    Добавляем пользователя в формате кортежа
    @param a: INT 1.юзер_id - id в телеграмме
    @param b: TEXT 2.first name в тг
    @param c: TEXT 3.last name в тг
    @param d: TEXT 4.username в дуолинго
    @param e: INTEGER 5.очки при регистрации 2000 (меняется кажд понедельник)
    @param f: INTEGER 6.очки на сайте        2001
    @param g: INTEGER 7.очки в игре          1
    """
    curs = conn.cursor()
    user = (a, b, c, d, e, f, g)
    curs.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?);", user)
    conn.commit()
    curs.close()


def update_data_user(user_id, e, f, g):
    """
    Обновляем данные пользователя в формате кортежа (юзер, очки на сайте, очки в игре)
    @param a: INT 1.юзер_id - id в телеграмме
    @param e: INTEGER 5.очки при регистрации 2000 (меняется кажд понедельник)
    @param f: INTEGER 6.очки на сайте        2001
    @param g: INTEGER 7.очки в игре          1
    """
    curs = conn.cursor()
    add_form = """UPDATE users SET
               experience_points_start = ?,
               experience_points_site = ?,
               experience_points_game = ?
               WHERE user_id = user_id"""
    add_points = (e, f, g)
    curs.execute(add_form, add_points)
    conn.commit()
    curs.close()


# Удаляем пользователя по имени
def del_user(user_id):
    curs = conn.cursor()
    command_delete = "DELETE FROM users WHERE user_id ="
    curs.execute(f"{command_delete} {user_id};")
    conn.commit()
    curs.close()


# Берем данные из таблицы
# запрос данных для одного чел
def result_one(user):
    curs = conn.cursor()
    curs.execute("SELECT * FROM users;")
    one_result = curs.fetchone()
    return one_result
    curs.close()


# запрос данных для первых десяти чел
def result_ten():
    curs = conn.cursor()
    curs.execute("SELECT * FROM users;")
    ten_results = curs.fetchmany(10)
    print(ten_results)
    curs.close()


# запрос данных обо всех участниках
def result_all():
    curs = conn.cursor()
    curs.execute("SELECT * FROM users;")
    all_results = curs.fetchall()
    print(all_results)
    curs.close()


# add_user(213123, 'Raduga', 'Prank You', 'Raduga_prankyou', 300000, 300000, 0)
# add_user(113232, 'Alex', 'New', 'nick', 1000, 1000, 0)
# update_data_user(113232, 1010, 1010, 10)
# del_user(213123)
# print(result_all())

# driver = webdriver.Chrome()
url = "https://en.duolingo.com/profile/"


def parser(base_url, name):
    """
    This function takes base_url and name user
    returns Total XP of user
    :param base_url:
    :param name:
    :return: bool, Total XP
    """
    driver = webdriver.Chrome()
    full_url = f"{base_url}{name}"
    driver.get(full_url)
    if driver.requests[0].response.status_code == http.HTTPStatus.OK:
        main_page = driver.page_source
        divs = main_page.split(">")
        for i in range(len(divs)):
            if "Total XP" in divs[i]:
                temp_str = divs[i - 2]
                total = int(temp_str[: temp_str.find("<") :])
                print(f"{name}: {total}")
                return True, total
    else:
        print(f"Error: {name}")
        return False, 0


@bot.message_handler(commands=["start"])
def reply_to_start(message):
    """
    Выводит список команд при отправлении команды старт.
    """
    commands_dict = {
        "/start": "Выводит это сообщение",
        "/take_part #username_в_Duolingo": "Заносит пользователя в таблицу участников",
        "/show": "Показывает опыт участников",
        "/show_winner": "Показывает победителя",
        "/help": "Выводит информацию о боте",
    }
    new_line = "\n"
    bot.send_message(
        message.chat.id,
        (
            "Бот для проведения соревнований в Duolingo.\n\n"
            f"""{new_line.join(f"{key} : {value}" for key, value in commands_dict.items())}"""
        ),
    )


@bot.message_handler(regexp=r"/take_part #\w+")
def reply_to_take_part(message):
    """
    Вводит сообщение от бота в зависимости от того, существует ли введённый им username.
    Заносит пользователя в БД при правильно введённом username.
    """
    us_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    text = message.text
    sharp_ind = text.find("#")
    duo_username = text[sharp_ind + 1 : :].strip()
    flag, total = parser(url, duo_username)

    if flag:
        add_user(us_id, first_name, last_name, duo_username, total, 0, 0)
        bot.reply_to(
            message,
            "Отлично! Ты теперь участник соревнования. Разгроми соперников!\U0001F608",
        )
    else:
        bot.reply_to(
            message,
            (
                "Такого username не существует. Попробуй ввести команду"
                "/take_part и свой username в формате /take_part #твой_username_в_Duolingo заново"
            ),
        )


@bot.message_handler(commands=["show"])
def show_table(message):
    """
    Показывает результаты количество опыта у участников на данный момент.
    """
    users_result = result_all()
    new_line = "\n"
    bot.send_message(
        message.chat.id,
        f"""{new_line.join(f"<a href='tg://user?id={data[0]}'>{data[1]} {data[2]}</a>  <b>{data[6]}</b>" for data in users_result)}""",
        parse_mode="HTML",
    )


@bot.message_handler(commands=["show_winner"])
def show_winner(message):
    """
    Выводит имя победителя и картинку для него.
    """
    pictures_links = (
        "https://i.pinimg.com/originals/1d/74/90/1d7490d7ca7d03e90a90bc4dcfabc4cc.jpg",
        "https://img1.fonwall.ru/o/br/harley-quinn-artist-digital-art.jpeg?route=thumb&h=350",
        "https://img1.fonwall.ru/o/pe/aquaman-superheroes-artist-artwork.jpeg?route=thumb&h=350",
        "https://img1.fonwall.ru/o/dq/wonder-woman-superheroes-artist-artwork-lnit.jpeg?route=thumb&h=350",
        "https://i.pinimg.com/736x/b0/7c/f0/b07cf003a2bb9351544f88e364d7787a.jpg",
    )

    ind = random.randrange(len(pictures_links))
    bot.send_photo(message.chat.id, pictures_links[ind])


@bot.message_handler(commands=["help"])
def help(message):
    """
    Выводит информацию о боте в ответ на команду /help.
    """
    commands_dict = {
        "/start": "Выводит это сообщение",
        "/take_part #username_в_Duolingo": "Заносит пользователя в таблицу участников",
        "/show": "Показывает опыт участников",
        "/show_winner": "Показывает победителя",
        "/help": "Выводит информацию о боте",
    }
    new_line = "\n"
    bot.send_message(
        message.chat.id,
        ("Бот для проведения соревнований в Duolingo.")(
            f"""{new_line.join(f"{key} : {value}" for key, value in commands_dict.items())}"""
        ),
    )


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        sleep(15)
