from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import Session
from sqlalchemy import select
from models import Level, Kanal
from sqlalchemy.ext.asyncio import AsyncSession


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



async def get_channel(session: AsyncSession):
    result = await session.execute(select(Kanal).where(Kanal.status == True))
    kanallar = result.scalars().all()
    return kanallar


def kanal_tugmalari(kanallar):
    buttons = []

    for kanal in kanallar:
        buttons.append([
            InlineKeyboardButton(
                text="📢 Kanalga obuna bo'lish",
                url=kanal.kanal_url
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="✅ Obuna bo'ldim",
            callback_data="check_subscription"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

