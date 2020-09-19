import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def creator(self, chat_id, user_id, first_name, last_name ):
        '''Create table'''
        with self.connection:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{chat_id}` (id INTEGER PRIMARY KEY AUTOINCREMENT , user_id VARCHAR, status INT, win INT DEFAULT (0) , first_name CHAR, last_name CHAR)""")

        #Create table time_counter
            a = []
            for i in self.cursor.execute(f"""SELECT `chat_id` FROM `time_counter`""").fetchall():
                a.append(i[0])
            if not int(chat_id) in a:
                self.cursor.execute(f"""INSERT INTO `time_counter` (`chat_id`, `date`) VALUES(?, ?)""",
                                        (chat_id, 0))

    def get_subscriptions(self, chat_id, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute(f"""SELECT `first_name`, `user_id`, `win` FROM `{chat_id}` WHERE `status` = ?""", (status,)).fetchall()

    def subscriber_exists(self, user_id, chat_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(f"""SELECT * FROM `{chat_id}` WHERE `user_id` = ?""", (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, chat_id, first_name, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute(f"""INSERT INTO `{chat_id}` (`user_id`, `first_name`, `status`) VALUES(?,?,?)""", (user_id, first_name, status))

    def update_subscription(self, user_id, chat_id, first_name, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(f"""UPDATE `{chat_id}` SET `status` = ?, `first_name` = ? WHERE `user_id` = ?""", (status, first_name, user_id))

    def choose_rat(self, chat_id, user_id):
        """Выбираем крысу"""
        with self.connection:
            return self.cursor.execute(f"""UPDATE `{chat_id}` SET `win` = `win` + ? WHERE `user_id` = ? """, (1, user_id))

    def check_time(self, chat_id, date):
        """Проверяем время"""

        if date != (self.cursor.execute("""SELECT `date` FROM `time_counter` WHERE `chat_id` = ?""", (chat_id,)).fetchone()[0]):
            self.cursor.execute("""UPDATE `time_counter` SET `date` = ? WHERE `chat_id` = ?""", (date, chat_id))
            return True

        return False
            
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()