from aiogram import Dispatcher
from aiogram.filters import Command,  StateFilter
from aiogram import F
from handler import start_command
dp = Dispatcher()

dp.message.register(start_command, Command("start"))
# dp.callback_query.register(handle_answer, StateFilter(SavollarStates.savollar))


