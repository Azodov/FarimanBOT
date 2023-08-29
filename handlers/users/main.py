from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsUser
from keyboards.inline.userKeyboards import menu_user
from loader import dp, db


@dp.message_handler(IsUser(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    else:
        await message.answer(f"👋 Assalomu alaykum, {message.from_user.full_name}!", reply_markup=menu_user)


@dp.callback_query_handler(IsUser(), text_contains="user:cancel", state="*")
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("❌ Bekor qilindi!", reply_markup=menu_user)
    await state.finish()


@dp.callback_query_handler(IsUser(), text_contains="user:done", state="*")
async def done_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    try:
        await call.message.edit_text("👍 O'zingizga kerakli bo'limni tanlang!", reply_markup=menu_user)
    except:
        await call.message.delete()
        await call.message.answer("👍 O'zingizga kerakli bo'limni tanlang!", reply_markup=menu_user)
    await state.finish()

