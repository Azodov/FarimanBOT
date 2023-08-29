from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS
from filters import IsUser
from keyboards.inline.userKeyboards import payment_type, cancel, back
from loader import dp, db, bot


@dp.callback_query_handler(IsUser(), text='user:pay', state='*')
async def location_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    await call.message.answer("📍 Yetkazish manzilini jo'nating", reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    ).add(
        KeyboardButton(text="Manzilni jo'natish", request_location=True)))

    await state.set_state('user:location:get')


@dp.message_handler(IsUser(), state='*', content_types=['location'])
async def pay(message: types.Message, state: FSMContext):
    await state.update_data(long=message.location.longitude, lat=message.location.latitude)
    await message.answer('Tolov turini tanlang', reply_markup=payment_type)


@dp.callback_query_handler(IsUser(), text='user:payment:card', state='*')
async def pay_card(call: types.CallbackQuery):
    user_cart = await db.select_user_cart(user_id=call.from_user.id, isPaid='SELECTED')
    price = 0
    for product in user_cart:
        price += (int(product['price']) * int(product['count']))
    await call.answer(cache_time=1)
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="♻️ To'lovni amalga oshirdim", callback_data="user:payment:success")
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
            ]
        ]
    )
    text = f"""
    <b>⚠️ Tolov turi Karta</b>\n
<b>💳 Karta raqam: <code>6262 7201 7451 0019</code></b>\n
<b>👤 To'lov qabul qiluvchi:</b> <code>MAXAMADALIYEV SAIDAKBAR</code>\n
<b>💵 To'lov miqdori: </b> <code>{price}</code> so'm\n\n
<b>💡 To'lovni amalga oshirgach "♻️ To'lovni amalga oshirdim" tugmasini bosing</b>
    """
    await call.message.answer(text, reply_markup=btn)


@dp.callback_query_handler(IsUser(), text='user:payment:success', state='*')
async def pay_success(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text('Juda soz, endi tolov qilganingizni tasdiqlash uchun chek rasmini yuboring...',
                                 reply_markup=cancel)
    await state.set_state('user:payment:success')


@dp.message_handler(IsUser(), state='user:payment:success', content_types=['photo'])
async def pay_success_photo(message: types.Message, state: FSMContext):
    await message.answer("Bizning tanlaganingiz uchun raxmat, tez orada siz bilan bog'lanamiz", reply_markup=back)
    user_info = await db.select_user(telegram_id=message.from_user.id)
    data = await state.get_data()
    amount = 0
    products = []
    user_cart = await db.select_user_cart(user_id=message.from_user.id, isPaid='SELECTED')
    for product in user_cart:
        await db.update_user_cart(user_id=message.from_user.id, product_id=product['product_id'], isPaid='PENDING')
        amount += (int(product['price']) * int(product['count']))
        products.append(
            f"📦 {product['name']} {product['massa']} - {product['count']} x {int(product['price'])}"
            f" = {int(product['price']) * int(product['count'])} so'm\n")

    for admin in ADMINS:
        await bot.send_photo(admin, message.photo[-1].file_id, caption=f"<b>♦️ Tolov turi Karta</b>\n"
                                                                       f"<b>📍 Viloyat: {user_info['region']}</b>\n"
                                                                       f"<b>👤 Foydalanuvchi: {user_info['fullname']}</b>\n"
                                                                       f"<b>📞 Telefon raqami: {user_info['phone_number']}</b>\n"
                                                                       f"<b>💵 To'lov miqdori: {amount} so'm</b>\n"
                                                                       f"📦 Mahsulotlar:\n"
                                                                       f"{''.join(products)}\n"
                                                                       f"📍Manzil 🔽🔽🔽")
        await bot.send_location(admin, latitude=data['lat'], longitude=data['long'])
    await state.finish()


@dp.callback_query_handler(IsUser(), text='user:payment:cash', state='*')
async def pay_cash(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    await call.message.answer("Siz bilan bog'lanishimiz uchun qo'shimcha telefon raqamingizni yuboring",
                              reply_markup=cancel)
    await state.set_state('user:payment:cash')


@dp.message_handler(IsUser(), state='user:payment:cash', content_types=['contact'])
@dp.message_handler(IsUser(), state='user:payment:cash', content_types=['text'])
async def pay_cash_contact(message: types.Message, state: FSMContext):
    await message.answer("Bizning tanlaganingiz uchun raxmat, tez orada siz bilan bog'lanamiz", reply_markup=back)
    user_info = await db.select_user(telegram_id=message.from_user.id)
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    data = await state.get_data()
    amount = 0
    products = []
    user_cart = await db.select_user_cart(user_id=message.from_user.id, isPaid='SELECTED')
    for product in user_cart:
        await db.update_user_cart(user_id=message.from_user.id, product_id=product['product_id'], isPaid='PENDING')
        amount += (int(product['price']) * int(product['count']))
        products.append(
            f"📦 {product['name']} {product['massa']} - {product['count']} x {int(product['price'])}"
            f" = {int(product['price']) * int(product['count'])} so'm\n")

    for admin in ADMINS:
        await bot.send_message(admin, f"<b>♦️ Tolov turi Naqd</b>\n"
                                      f"<b>📍 Viloyat: {user_info['region']}</b>\n"
                                      f"<b>👤 Foydalanuvchi: {user_info['fullname']}</b>\n"
                                      f"<b>📞 Telefon raqami: {user_info['phone_number']}</b>\n"
                                      f"<b>📞 Qo'shimcha raqami: {phone_number}</b>\n"
                                      f"<b>💵 To'lov miqdori: {amount} so'm</b>\n"
                                      f"📦 Mahsulotlar:\n"
                                      f"{''.join(products)}\n"
                                      f"📍Manzil 🔽🔽🔽")
        await bot.send_location(admin, latitude=data['lat'], longitude=data['long'])
    await state.finish()
