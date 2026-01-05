from telebot import TeleBot, types
from db.db import Database
from essence import User, Reminder
import datetime
import calendar
import time

#function for processing user requests
def register_handlers(bot: TeleBot):
    #function for time format check
    def examination_date_type(user_time):
        time_format = "%H:%M"
        try:
            datetime.datetime.strptime(user_time, time_format)
            return True
        except:
            return False
        
    #test function(get all DB or remove keyboard or delete accont(by user_name))
    @bot.message_handler(commands=["test"])
    def test(message):
        if message.text == "🔙Back" or message.text == "back":
            handle_button(message)
            return
        
        Database.create_table()
        all_users = Database.get_all_users()
        print("users: ", all_users)

        all_reminders = Database.get_all_reminder()
        print("remonders: ", all_reminders)

        now = datetime.datetime.now()
        print("now: ", now)

        #remove keyboard
        # markup = types.ReplyKeyboardRemove()
        # bot.send_message(message.chat.id, """keyboard is remove""", reply_markup=markup)

        #delete account
        # telegram_id = str(message.chat.id)
        # User = Database.get_user_by_telegram_id(telegram_id)
        # Database.delete_account(User.user_name)

    #choose day
    @bot.callback_query_handler(
        func=lambda call: call.data
        in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
    )
    #Button press handler for weekend day later text for user and choose time
    def callback_query_add_reminder(call):
        message = call.message
        global day_reminder
        if call.data == "monday": 
            bot.send_message(message.chat.id, """OK,  Monday""")
            day_reminder = 0
        elif call.data == "tuesday":  
            bot.send_message(message.chat.id, """OK,  Tuesday""")
            day_reminder = 1
        elif call.data == "wednesday":  
            bot.send_message(message.chat.id, """OK,  Wednesday""")
            day_reminder = 2
        elif call.data == "thursday": 
            bot.send_message(message.chat.id, """OK,  Thursday""")
            day_reminder = 3
        elif call.data == "friday": 
            bot.send_message(message.chat.id, """OK,  Friday""")
            day_reminder = 4
        elif call.data == "saturday":  
            bot.send_message(message.chat.id, """OK,  Saturday""")
            day_reminder = 5
        elif call.data == "sunday": 
            bot.send_message(message.chat.id, """OK,  Sunday""")
            day_reminder = 6
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """what time?""")
        bot.register_next_step_handler(message, processing_time_reminder)

    #delete reminder by day and time
    @bot.callback_query_handler(
        func=lambda call: call.data
        in [
            "delete_monday",
            "delete_tuesday",
            "delete_wednesday",
            "delete_thursday",
            "delete_friday",
            "delete_saturday",
            "delete_sunday",
        ]
    )
    #Button press handler for weekend day
    def callback_query_delete_reminder(call):
        message = call.message
        global day_reminder
        if call.data == "delete_monday":  
            bot.send_message(message.chat.id, """OK,Monday""")
            day_reminder = 0
        elif call.data == "delete_tuesday": 
            bot.send_message(message.chat.id, """OK,Tuesday""")
            day_reminder = 1
        elif call.data == "delete_wednesday": 
            bot.send_message(message.chat.id, """OK,Wednesday""")
            day_reminder = 2
        elif call.data == "delete_thursday": 
            bot.send_message(message.chat.id, """OK,Thursday""")
            day_reminder = 3
        elif call.data == "delete_friday": 
            bot.send_message(message.chat.id, """OK,Friday""")
            day_reminder = 4
        elif call.data == "delete_saturday": 
            bot.send_message(message.chat.id, """OK,Saturday""")
            day_reminder = 5
        elif call.data == "delete_sunday": 
            bot.send_message(message.chat.id, """OK,Sunday""")
            day_reminder = 6
        bot.delete_message(message.chat.id, message.message_id)
        processing_day_reminder_delete(message)

    #delete reminder if any
    @bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
    def callback_query_delete_reminder_time(call):
        message = call.message
        global id_reminder, lst_reminder
        try:
            idx = int(call.data.replace("del_", ""))
            id_reminder = idx - 1
            delete_reminder_processing_time(message)
            bot.delete_message(message.chat.id, message.message_id)
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Error deleting reminder")

    #base function
    @bot.callback_query_handler(
        func=lambda call: call.data
        in ["help", "start", "add_reminder", "delete_reminder"]
    )
    def callback_query_help(call):
        message = call.message
        if call.data == "help":
            bot.delete_message(message.chat.id, message.message_id)
            help(message)
        elif call.data == "start":
            bot.delete_message(message.chat.id, message.message_id)
            start(message)
        elif call.data == "add_reminder":
            bot.delete_message(message.chat.id, message.message_id)
            add_reminder(message)
        elif call.data == "delete_reminder":
            bot.delete_message(message.chat.id, message.message_id)
            delete_reminder(message)

    #start function
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "Hello! Enter your name")
        bot.register_next_step_handler(message, register_user)

    #registration new user
    def register_user(message):
        telegram_id = str(message.chat.id)
        user_name = message.text
        if (
            Database.get_user_by_user_name(user_name) is not None
            and telegram_id != Database.get_user_by_user_name(user_name).telegram_id
        ):
            bot.send_message(
                message.chat.id, "User with that name is exists, please enter another one."
            )
            bot.register_next_step_handler(message, start)
            return
        if Database.get_user_by_user_name(user_name) is None:
            user = User(user_name, telegram_id)
            Database.add_user(user)
        markup = types.InlineKeyboardMarkup()
        help_bttn = types.InlineKeyboardButton(text="help", callback_data="help")
        markup.add(help_bttn)
        bot.send_message(
            message.chat.id, "ready, show commands?", reply_markup=markup
        )
        start_help_back_button(message)

    #add button '🔙Back'
    def start_help_back_button(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("🔙Back")
        markup.add(back)
        bot.send_message(
            message.chat.id,
            "To access Help from anywhere, simply click the '🔙Back' button or type the word 'Back'",
            reply_markup=markup,
        )
    #Button press back for weekend day
    @bot.message_handler(
        func=lambda message: message.text == "🔙Back" or message.text == "Back"
    )
    def handle_button(message):
        bot.send_message(message.chat.id, "OK, back you to Help")
        help(message)

    #function help
    @bot.message_handler(commands=["help"])
    def help(message):
        markup = types.InlineKeyboardMarkup()

        help_bttn = types.InlineKeyboardButton(text="🆘help", callback_data="help")
        start_bttn = types.InlineKeyboardButton(text="🚀start", callback_data="start")

        add_reminder_bttn = types.InlineKeyboardButton(
            text="📅✅Add reminder", callback_data="add_reminder"
        )
        delete_reminder_bttn = types.InlineKeyboardButton(
            text="📅❌Delete reminder", callback_data="delete_reminder"
        )

        markup.add(help_bttn, start_bttn)
        markup.add(add_reminder_bttn)
        markup.add(delete_reminder_bttn)

        bot.send_message(
            message.chat.id,
            """📌Command for bot:
    🆘help — Command reference
    🚀start — start bot
    📅✅Add reminder — Add reminder
    📅❌Delete reminder — Delete reminder
                        """,
            reply_markup=markup,
        )

    #create new reminder
    @bot.message_handler(commands=["add_reminder"])
    def add_reminder(message):
        markup = types.InlineKeyboardMarkup()

        monday = types.InlineKeyboardButton(
            text="📅🟦Monday", callback_data="monday"
        )
        tuesday = types.InlineKeyboardButton(
            text="📅🟧Tuesday", callback_data="tuesday"
        )

        wednesday = types.InlineKeyboardButton(
            text="📅🟩Wednesday", callback_data="wednesday"
        )
        thursday = types.InlineKeyboardButton(
            text="📅🟥Thursday", callback_data="thursday"
        )

        friday = types.InlineKeyboardButton(text="📅🟪Friday", callback_data="friday")
        saturday = types.InlineKeyboardButton(
            text="📅🟫Saturday", callback_data="saturday"
        )

        sunday = types.InlineKeyboardButton(
            text="📅⬛Sunday", callback_data="sunday"
        )

        markup.add(monday, tuesday)
        markup.add(wednesday, thursday)
        markup.add(friday, saturday)
        markup.add(sunday)

        bot.send_message(
            message.chat.id,
            "Select the days you want reminders.",
            reply_markup=markup,
        )

    #register time
    def request_time(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        bot.send_message(message.chat.id, """What time?""")
        bot.register_next_step_handler(message.chat.id, processing_time_reminder)

    #processing time
    def processing_time_reminder(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        global time_reminder
        time_reminder = message.text
        if not examination_date_type(time_reminder):
            bot.send_message(message.chat.id, "Wrong time format")
            bot.register_next_step_handler(message, processing_time_reminder)
            return None

        bot.send_message(message.chat.id, """What should I call the reminder?""")
        bot.register_next_step_handler(message, processing_text_reminder)

    #processing description
    def processing_text_reminder(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        global text_reminder
        text_reminder = message.text
        save_reminder(message)

    def save_reminder(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminder = Reminder(user.user_name, day_reminder, time_reminder, text_reminder)
        Database.add_reminder(reminder)
        bot.send_message(message.chat.id, "I wrote it down and will remind you")

    #function for delete reminder
    @bot.message_handler(commands=["delete_reminder"])
    def delete_reminder(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        markup = types.InlineKeyboardMarkup()

        monday = types.InlineKeyboardButton(
            text="📅🟦Monday", callback_data="delete_monday"
        )
        tuesday = types.InlineKeyboardButton(
            text="📅🟧Tuesday", callback_data="delete_tuesday"
        )

        wednesday = types.InlineKeyboardButton(
            text="📅🟩Wednesday", callback_data="delete_wednesday"
        )
        thursday = types.InlineKeyboardButton(
            text="📅🟥Thursday", callback_data="delete_thursday"
        )

        friday = types.InlineKeyboardButton(
            text="📅🟪Friday", callback_data="delete_friday"
        )
        saturday = types.InlineKeyboardButton(
            text="📅🟫Saturday", callback_data="delete_saturday"
        )

        sunday = types.InlineKeyboardButton(
            text="📅⬛Sunday", callback_data="delete_sunday"
        )

        markup.add(monday, tuesday)
        markup.add(wednesday, thursday)
        markup.add(friday, saturday)
        markup.add(sunday)

        bot.send_message(
            message.chat.id,
            "Select the days on which you no longer want reminders",
            reply_markup=markup,
        )

    #processinf day
    def processing_day_reminder_delete(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminders = Database.get_reminders_by_user_name_and_day(
            user.user_name, day_reminder
        )
        day_name = calendar.day_name[day_reminder]
        global num_reminders
        num_reminders = 0
        global lst_reminder
        lst_reminder = []
        if reminders is None:
            bot.send_message(
                message.chat.id, f"There are no reminders for the selected day {day_name}"
            )
            return
        for reminder in reminders:
            print_text = f"{day_name} - {reminder.time_reminder}"
            num_reminders += 1
            name_delete = f"del_{num_reminders}"
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(
                text="delete", callback_data=name_delete
            )
            markup.add(button)
            bot.send_message(message.chat.id, print_text, reply_markup=markup)
            lst_reminder.append(reminder)

    #delete reminder final
    def delete_reminder_processing_time(message):
        if message.text == "🔙Back" or message.text == "Back":
            handle_button(message)
            return
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminders = Database.get_reminders_by_user_name_and_day(
            user.user_name, day_reminder
        )
        reminder = reminders[id_reminder]
        Database.delete_reminder_by_user_name_day_time_reminder(
            reminder.user_name, reminder.day_reminder, reminder.time_reminder
        )
        bot.send_message(message.chat.id, "deleted the reminder")

#cheking reminder every minutes
def check_reminder_every_minutes(bot: TeleBot):
    while True:
        now = datetime.datetime.now()
        today = now.weekday()
        time_now = now.strftime("%H:%M")
        all_reminders = Database.get_all_reminder()
        if all_reminders is not None:
            for reminder in all_reminders:
                if (
                    int(reminder.day_reminder) == today
                    and reminder.time_reminder == time_now
                ):
                    user = Database.get_user_by_user_name(reminder.user_name)
                    bot.send_message(
                        user.telegram_id, f"⏰reminder!{reminder.text_reminder}"
                    )
        time.sleep(60)
