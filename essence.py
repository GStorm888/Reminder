from dataclasses import dataclass


@dataclass
class User:
    user_name: str
    telegram_id: str
    id: int = None


@dataclass
class Reminder:
    user_name: str
    day_reminder: int
    time_reminder: str
    text_reminder: str
    id: int = None
