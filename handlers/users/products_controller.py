from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters import IsUser
from keyboards.inline.userKeyboards import cart, cancel
from loader import dp, db


@dp.callback_query_handler(IsUser(), text_contains="user:products", state="*")
async def products_handler(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    products_list = await db.select_all_products()
    btn = InlineKeyboardMarkup(row_width=1)
    for product in products_list:
        btn.insert(InlineKeyboardButton(text=f"{product[1]} {product[3]}", callback_data=f"user:product:{product[0]}"))
    btn.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel"))
    await call.message.delete()
    await call.message.answer("📦 Mahsulotlar ro'yxati:", reply_markup=btn)


@dp.callback_query_handler(IsUser(), text_contains="user:product", state="*")
async def product_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    product_id = call.data.split(":")[-1]
    product = await db.select_product(id=int(product_id))
    await state.update_data(id=product_id)
    btn = [
        [
            InlineKeyboardButton(text="➕ Savatchaga qo'shish", callback_data=f"user:add_to_cart:{product_id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:products")
        ]
    ]
    await call.message.delete()
    await call.message.answer_photo(photo=product[2], caption=f"<b>{product[1]}</b>\n\n"
                                                              f"⚖️ Massa: <b>{product[3]}</b>\n"
                                                              f"💲 Narxi: <b>{product[4]}</b> so'm\n"
                                                              f"📝 Izoh: <b>{product[5]}</b>",
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=btn))


@dp.callback_query_handler(IsUser(), text_contains="user:add_to_cart", state="*")
async def add_to_cart_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    product_id = call.data.split(":")[-1]
    user_id = call.from_user.id
    await state.update_data(product_id=product_id)
    await state.update_data(user_id=user_id)
    await call.message.delete()
    await call.message.answer("🔟 Mahsulotlar sonini kiriting:", reply_markup=cancel)
    await state.set_state("add_to_cart")


@dp.message_handler(IsUser(), state="add_to_cart")
async def add_to_cart_handler(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
    except ValueError:
        await message.answer("❗️ Son kiriting!")
        return
    if count <= 0:
        await message.answer("❗️ Son musbat bo'lishi kerak!")
        return
    data = await state.get_data()
    product_id = data.get("product_id")
    user_id = data.get("user_id")
    await db.add_to_cart(user_id=user_id, product_id=int(product_id), count=int(count), isPaid='SELECTED')
    await message.answer("✅ Savatchaga qo'shildi!", reply_markup=cart)
    await state.finish()
    await state.reset_data()
