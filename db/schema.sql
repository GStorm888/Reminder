CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    telegram_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, 
    day_reminder INTEGER NOT NULL,
    time_reminder TEXT NOT NULL, 
    text_reminder TEXT NOT NULL,
    FOREIGN KEY (user_name) REFERENCES users(user_name)
)