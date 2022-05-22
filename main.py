import telebot
from time import sleep

bot = telebot.TeleBot('')


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
