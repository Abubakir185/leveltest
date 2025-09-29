from aiogram.types import Message
from buttons import make_level_keyboard, get_levels, get_channel, kanal_tugmalari
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import random
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import insert, select
from database import Session
from models import User, Level, Question
from bot import Bot
from functions import Check_subscription


class TestState(StatesGroup):
    testing = State()

async def start_command(msg: Message, state: FSMContext, bot: Bot):
    session = Session()

    # 1. Obuna tekshiruv
    is_member = await Check_subscription(bot, msg.from_user.id)
    if not is_member:
        kanallar = await get_channel(session)
        await msg.answer(
            "!Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=kanal_tugmalari(kanallar)
        )
        session.close()
        return

    user = session.scalar(select(User).where(User.telegram_id == msg.from_user.id))
    if not user:
        yangi_user = User(
            telegram_id=msg.from_user.id,
            full_name=msg.from_user.full_name
        )
        session.add(yangi_user)
        session.commit()

    session.close()

    levels = await get_levels()
    buttons = make_level_keyboard(levels)

    await msg.answer("Botga xush kelibsiz!")
    await msg.answer("Qaysi level boyicha test yechib korasiz", reply_markup=buttons)


# result = session.execute(select(Question).where(Question.level_id == 1))
# questions = result.scalars().all()

# if not questions:
#     await msg.answer("Savollar topilmadi.")
#     session.close()
#     return

# await state.update_data(questions=questions, index=0, correct=0)

# await send_question(msg.chat.id, state)
# await TestState.testing.set()

# async def start_handler(msg: Message, state: FSMContext):


#     async with Session() as session:
#         result = await session.execute(select(Question).where(Question.level_id == 1))
#         questions = result.scalars().all()

#     if not questions:
#         await msg.answer("Savollar topilmadi.")
#         return

#     await state.update_data(questions=questions, index=0, correct=0)
#     await send_question(msg.chat.id, state)
#     await TestState.testing.set()

# # Savol yuborish
# async def send_question(chat_id: int, state: FSMContext, callback: CallbackQuery):
#     data = await state.get_data()
#     index = data["index"]
#     questions = data["questions"]

#     if index >= len(questions):
#         await finish_test(chat_id, state)
#         return

#     q = questions[index]
#     # await bot.send_message(chat_id, f"<b>{q.text}</b>", reply_markup=question_keyboard(q))
#     await Bot.send_message(chat_id, f"<b>{q.text}</b>", reply_markup=question_keyboard(q))

# # Callback qayta ishlash
# @dp.callback_query(TestState.testing)
# async def handle_answer(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     index = data["index"]
#     questions = data["questions"]
#     selected = callback.data
#     question = questions[index]

#     is_correct = selected == question.correct_option
#     if is_correct:
#         data["correct"] += 1
#         await callback.answer("✅ To‘g‘ri!")
#     else:
#         await callback.answer("❌ Xato!")

#     # Javobni saqlash
#     async with Session() as session:
#         user = await session.scalar(select(User).where(User.telegram_id == callback.from_user.id))
#         answer = UserAnswer(
#             user_id=user.id,
#             question_id=question.id,
#             selected_option=selected,
#             is_correct=is_correct
#         )
#         session.add(answer)
#         await session.commit()

#     # Keyingi savolga o‘tish
#     data["index"] += 1
#     await state.set_data(data)
#     await send_question(callback.message.chat.id, state)

# # Test tugashi
# async def finish_test(chat_id: int, state: FSMContext):
#     data = await state.get_data()
#     correct = data["correct"]
#     total = len(data["questions"])
#     text = f"✅ Siz {total} ta savoldan <b>{correct}</b> tasiga to‘g‘ri javob berdingiz."

#     await bot.send_message(chat_id, text)
#     await state.clear()

# # Ishga tushirish
# async def main():
#     print("Bot ishga tushdi...")
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())
