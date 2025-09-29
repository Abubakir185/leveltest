import logging
from aiogram import Bot 
from models import Kanal
from database import Session
from sqlalchemy import select

async def Check_subscription(bot: Bot, user_id: int):
    session = Session()
    kanallar = session.execute(select(Kanal)).scalars().all()

    for kanal in kanallar:
        try:
            member = await bot.get_chat_member(chat_id=kanal.kanal_id, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            logging.error(f"Error checking subscription: {e}")
            return False
    return True
