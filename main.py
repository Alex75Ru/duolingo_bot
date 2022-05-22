import sqlite3
from selenium import webdriver

# Создаем файл с БД
conn = sqlite3.connect('list_users.db')

# Создаем курсор который будет делать запросы в БД
cur = conn.cursor()

# Создаем таблицу в БД 5 колонок
# 1.юзер_id, 2.имя, 3.очки при регистрации, 4.очки на сайте, 5.очки в игре
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INT PRIMARY KEY,
   name TEXT,
   experience_points_start INTEGER,
   experience_points_site INTEGER,
   experience_points_game INTEGER);
""")
conn.commit()

# Добавляем пользователя (образец)
# user = ('00002', 'Raduga', '300000', '300000', '0')
# cur.execute("""INSERT INTO users(userid, fname, lname, gender)
#    VALUES('00001', 'Alex', 'Smith', 'male');""")
# conn.commit()

# Добавляем пользователя в формате кортежа
def add_user(a, b, c, d, e):
    user = (a, b, c, d, e)
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user)
    conn.commit()

# Удаляем пользователя по имени
def del_user(user):
    cur.execute("DELETE FROM users WHERE name=user;")
    conn.commit()

# Берем данные из таблицы
# запрос данных для одного чел
def result_one(user):
    cur.execute("SELECT * FROM users;")
    one_result = cur.fetchone()
    print(one_result)

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
    :return: {user: Total XP}
    """
    full_url = f"{base_url}{name}"
    driver.get(full_url)
    main_page = driver.page_source
    divs = main_page.split(">")
    for i in range(len(divs)):
        if "Total XP" in divs[i]:
            temp_str = divs[i-2]
            total = int(temp_str[:temp_str.find("<"):])
            print(total)
            return {name: total}


parser(url, "username")
