import asyncio
from bot import bot
from dispatcher import dp
from models import Base
from database import engine
from bot import set_commands
from crud import add_level, add_question
import concurrent.futures

Base.metadata.create_all(engine)


async def on_start():
    await set_commands()
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        # Avval Level larni qo‘shamiz
        await loop.run_in_executor(pool, add_level)

        # So‘ngra Question larni qo‘shamiz
        await loop.run_in_executor(pool, add_question)

    print("bot has been started")



async def main():
    dp.startup.register(on_start)
    await dp.start_polling(bot)


asyncio.run(main()) 
