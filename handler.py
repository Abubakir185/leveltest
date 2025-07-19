from aiogram.types import Message
from buttons import make_level_keyboard, get_levels
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import random
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import insert, select
from database import Session
from models import User, Level

async def start_command(msg: Message):
        await msg.answer(f"{msg.from_user.full_name} botga xush kelibsiz!")
        levels = await get_levels()
        keyboard = make_level_keyboard(levels)
        await msg.answer("Qaysi level boyicha test yechib ko'rasiz?", reply_markup=keyboard)

        session = Session()
        query = insert(User).values(telegram_id=msg.from_user.id, full_name=msg.from_user.full_name)
        session.execute(query)
        session.commit()
        session.close()



class SavollarStates(StatesGroup):
    savollar = State()



