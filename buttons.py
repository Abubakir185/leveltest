from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import Session
from sqlalchemy import select
from models import Level


async def get_levels():
    session = Session()
    query = select(Level)
    result = session.execute(query)
    levels = result.scalars().all()

    return levels



def make_level_keyboard(levels: list[Level]) -> ReplyKeyboardMarkup:
    keyboard = []
    for level in levels:
        keyboard.append([KeyboardButton(text=level.name)])  
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
