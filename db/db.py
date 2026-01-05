import sqlite3
from essence import User, Reminder


class Database:
    SCHEMA = "db/schema.sql"
    DATABASE = "db/reminder.db"

    #a function to start doing something
    @staticmethod
    def execute(sql, params=()):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(sql, params)

        connection.commit()

    #creating table function
    @staticmethod
    def create_table():
        with open(Database.SCHEMA) as schema_file:
            connection = sqlite3.connect(Database.DATABASE)
            cursor = connection.cursor()
            cursor.executescript(schema_file.read())
            connection.commit()
            connection.close()

    #function for add user in table 'users'
    @staticmethod
    def add_user(user: User):
        Database.execute(
            "INSERT INTO users (user_name, telegram_id) VALUES (?, ?)",
            [
                user.user_name,
                user.telegram_id,
            ],
        )
        return True

    # function for getting all users from table 'users'
    @staticmethod
    def get_all_users():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")

        all_users = cursor.fetchall()
        users = []
        for id, user_name, telegram_user_id in all_users:
            user = User(user_name, telegram_user_id, id)
            users.append(user)
        if len(users) == 0:
            return None
        return users

    #serch and get user by telegram id in table 'users'
    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE telegram_id=?", [telegram_id])

        all_users = cursor.fetchall()
        users = []
        for id, user_name, telegram_user_id in all_users:
            user = User(user_name, telegram_user_id, id)
            users.append(user)
        if len(users) == 0:
            return None
        return user

    #search and get user by user name in table 'users'
    @staticmethod
    def get_user_by_user_name(user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_name=?", [user_name])

        all_users = cursor.fetchall()
        users = []
        for id, user_name, telegram_user_id in all_users:
            user = User(user_name, telegram_user_id, id)
            users.append(user)
        if len(users) == 0:
            return None
        return user

    #add reminder in table 'reminders'
    @staticmethod
    def add_reminder(reminder: Reminder):
        Database.execute(
            "INSERT INTO reminders (user_name, day_reminder, time_reminder, text_reminder) VALUES (?, ?, ?, ?)",
            [
                reminder.user_name,
                reminder.day_reminder,
                reminder.time_reminder,
                reminder.text_reminder,
            ],
        )
        return True

    #search and get all reminders in table 'reminders'
    @staticmethod
    def get_all_reminder():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM reminders")

        all_reminders = cursor.fetchall()
        reminders = []
        for id, user_name, day_reminder, time_reminder, text_reminder in all_reminders:
            reminder = Reminder(
                user_name, day_reminder, time_reminder, text_reminder, id
            )
            reminders.append(reminder)
        if len(reminders) == 0:
            return None
        return reminders

    #search and get reminder by user name and day reminder in table 'reminders'
    @staticmethod
    def get_reminders_by_user_name_and_day(user_name, day_reminder):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM reminders WHERE user_name=? AND day_reminder=?",
            [user_name, day_reminder],
        )

        all_reminders = cursor.fetchall()
        reminders = []
        for id, user_name, day_reminder, time_reminder, text_reminder in all_reminders:
            reminder = Reminder(
                user_name, day_reminder, time_reminder, text_reminder, id
            )
            reminders.append(reminder)
        if len(reminders) == 0:
            return None
        return reminders

    #serch and delete reminder by all field in table 'reminders'
    @staticmethod
    def delete_reminder_by_user_name_day_time_reminder(
        user_name, day_reminder, time_reminder
    ):
        Database.execute(
            """DELETE FROM reminders WHERE user_name=? AND day_reminder=? AND time_reminder=?""",
            [user_name, day_reminder, time_reminder],
        )
        return True

    #All the specifications are met, but the useful function only works in test mode.
    #deleting a profile and all reminders
    @staticmethod  
    def delete_account(user_name):
        Database.execute("""DELETE FROM users WHERE user_name=?""", [user_name])
        Database.execute("""DELETE FROM reminders WHERE user_name=?""", [user_name])
        return True