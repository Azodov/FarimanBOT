from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, InlineKeyboardButton, InlineKeyboardMarkup

from filters import IsGuest
from keyboards.inline.userKeyboards import menu_user
from loader import dp, db


@dp.message_handler(IsGuest(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if message.get_args():
        await db.update_admin(telegram_id=int(message.from_user.id), otp=int(message.get_args()), action=None)
        await message.answer(f"Salom Admin, {message.from_user.full_name}!")
    else:
        await message.answer(f"Salom Mehmon\nBotdan foydalanish uchun telefon raqamingizni yuboring\n"
                             , reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)
            ))

    await state.set_state("get_phone_number")


@dp.message_handler(IsGuest(), content_types=ContentType.CONTACT, state="get_phone_number")
@dp.message_handler(IsGuest(), state="get_phone_number", content_types=ContentType.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)
    await message.answer(f"✍️ To'liq ismingizni kiriting")
    await state.set_state("get_fullname")


@dp.message_handler(IsGuest(), state="get_fullname", content_types=ContentType.TEXT)
async def get_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(fullname=fullname)
    regions_btn = InlineKeyboardMarkup(row_width=1)
    regions_btn.add(InlineKeyboardButton(text="🇺🇿 Toshkent", callback_data="region:Toshkent"),
                    InlineKeyboardButton(text="🇺🇿 Andijon", callback_data="region:Andijon"),
                    InlineKeyboardButton(text="🇺🇿 Buxoro", callback_data="region:Buxoro"),
                    InlineKeyboardButton(text="🇺🇿 Farg'ona", callback_data="region:Farg'ona"),
                    InlineKeyboardButton(text="🇺🇿 Jizzax", callback_data="region:Jizzax"),
                    InlineKeyboardButton(text="🇺🇿 Xorazm", callback_data="region:Xorazm"),
                    InlineKeyboardButton(text="🇺🇿 Namangan", callback_data="region:Namangan"),
                    InlineKeyboardButton(text="🇺🇿 Navoiy", callback_data="region:Navoiy"),
                    InlineKeyboardButton(text="🇺🇿 Qashqadaryo", callback_data="region:Qashqadaryo"),
                    InlineKeyboardButton(text="🇺🇿 Samarqand", callback_data="region:Samarqand"),
                    InlineKeyboardButton(text="🇺🇿 Sirdaryo", callback_data="region:Sirdaryo"),
                    InlineKeyboardButton(text="🇺🇿 Surxondaryo", callback_data="region:Surxondaryo"),
                    InlineKeyboardButton(text="🇺🇿 Qoraqalpog'iston", callback_data="region:Qoraqalpog'iston"))

    await message.answer(f"📍 Viloyatingizni tanlang", reply_markup=regions_btn)
    await state.set_state("get_region")


@dp.callback_query_handler(IsGuest(), text_contains="region:", state="get_region")
async def get_region(call: types.CallbackQuery, state: FSMContext):
    region = call.data.split(":")[-1]
    data = await state.get_data()
    try:
        await db.add_user(fullname=data.get("fullname"), telegram_id=call.from_user.id, language="uz",
                          region=region, phone_number=data.get("phone_number"))
        await call.message.edit_text(f"✅ Tabriklaymiz siz ro'yxatdan o'tdingiz!", reply_markup=menu_user)
        await state.finish()
    except Exception as err:
        print(err)
        await call.message.answer(f"❌ Xatolik yuz berdi, iltimos qaytadan urinib ko'ring!")
        await state.finish()
