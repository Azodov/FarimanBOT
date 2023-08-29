from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsAdmin
from loader import dp, db


@dp.message_handler(IsAdmin(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Salom Admin, {message.from_user.full_name}!")
