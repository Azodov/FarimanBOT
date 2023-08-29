import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes
from aiogram.utils import exceptions

from filters import IsSuperAdmin
from keyboards.inline.superAdminKeyboards import cancel, back
from loader import db, dp, bot


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:send_ads", state="*")
async def send_ads(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.answer("Xabarni yuboring:", reply_markup=cancel)
    await state.set_state("superadmin:ads:get")


@dp.message_handler(IsSuperAdmin(), state="superadmin:ads:get", content_types=ContentTypes.ANY)
async def send_message(message: Message):
    users = await db.select_all_users()

    success = 0
    removed = 0

    await message.answer(f"⚠️ Xabar {len(users)} ta foydalunvchiga yuborilmoqda...\n"
                         f"🕔 Bu jarayon bir oz vaqt olishi mumkin, iltimos kuting...")

    for user in users:
        user_id = user['telegram_id']
        try:
            await bot.copy_message(user_id, message.chat.id, message.message_id)
            success += 1
        except exceptions.BotBlocked:
            await db.delete_user(telegram_id=user_id)
            removed += 1
        except exceptions.ChatNotFound:
            await db.delete_user(telegram_id=user_id)
            removed += 1
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)
            await bot.copy_message(user_id, message.chat.id, message.message_id)
            success += 1
        except exceptions.UserDeactivated:
            await db.delete_user(telegram_id=user_id)
            removed += 1

    await message.answer(
        text=f"✅ Xabar {success} ta foydalanuvchiga yetkazildi.\n"
             f"❌ {removed} ta foydalanuvchi botdan o'chirildi."
        , reply_markup=back)
