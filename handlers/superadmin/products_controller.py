from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ContentTypes

from filters import IsSuperAdmin
from keyboards.inline.superAdminKeyboards import menu_super_admin, cancel
from loader import db, dp, bot


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:products", state="*")
async def fn_products_list(call: CallbackQuery):
    await call.answer(cache_time=1)
    products_list = await db.select_all_products()
    btn = []
    for product in products_list:
        btn.append(
            [InlineKeyboardButton(text=f"{product[1]} {product[3]}", callback_data=f"superadmin:product:{product[0]}")])
    btn.append([InlineKeyboardButton(text="➕ Yangi mahsulot qo'shish", callback_data="superadmin:add_product")])
    btn.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="superadmin:cancel")])
    try:
        await call.message.edit_text("🛒 Mahsulotlar ro'yxati:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btn))
    except:
        await call.message.delete()
        await call.message.answer("🛒 Mahsulotlar ro'yxati:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btn))


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:add_product", state="*")
async def add_product(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("📝 Yangi mahsulot nomini kiriting:", reply_markup=cancel)
    await state.set_state("add_product:name")


@dp.message_handler(IsSuperAdmin(), state="add_product:name")
async def get_product_name(message: Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    await message.answer("🖼 Mahsulot rasmini kiriting:", reply_markup=cancel)
    await state.set_state("add_product:photo")


@dp.message_handler(IsSuperAdmin(), state="add_product:photo", content_types=ContentTypes.PHOTO)
async def get_product_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await message.answer("⚖️ Mahsulot massasini kiriting (Masalan: 100g):", reply_markup=cancel)
    await state.set_state("add_product:massa")


@dp.message_handler(IsSuperAdmin(), state="add_product:massa")
async def get_product_massa(message: Message, state: FSMContext):
    massa = message.text
    await state.update_data(massa=massa)
    await message.answer("💵 Mahsulot narxini kiriting:", reply_markup=cancel)
    await state.set_state("add_product:price")


@dp.message_handler(IsSuperAdmin(), state="add_product:price")
async def get_product_price(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await message.answer("✍️ Mahsulotni tavsifini kiriting:", reply_markup=cancel)
    await state.set_state("add_product:desc")


@dp.message_handler(IsSuperAdmin(), state="add_product:desc")
async def get_product_desc(message: Message, state: FSMContext):
    desc = message.text
    data = await state.get_data()
    await db.add_product(name=data["product_name"], massa=data['massa'], file_id=data["file_id"], price=data["price"],
                         description=desc)
    await message.answer("✅ Mahsulot muvaffaqiyatli qo'shildi!", reply_markup=menu_super_admin)
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:product", state="*")
async def get_product(call: CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=1)
    product_id = call.data.split(":")[-1]
    product = await db.select_product(id=int(product_id))
    await bot.send_photo(chat_id=call.message.chat.id, photo=product[2],
                         caption=f"<b>{product[1]}</b>\n\n"
                                 f"<b>⚖️ Massa:</b> {product[3]}\n"
                                 f"<b>💲 Narxi:</b> {product[4]}\n"
                                 f"<b>📝 Tavsifi:</b> {product[5]}",
                         parse_mode="html",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [
                                 InlineKeyboardButton(text="📈 Narxni o'zgartirish",
                                                      callback_data=f"superadmin:edit_price:{product[0]}")
                             ],
                             [
                                 InlineKeyboardButton(text="📝 Tavsifni o'zgartirish",
                                                      callback_data=f"superadmin:edit_desc:{product[0]}")
                             ],
                             [
                                 InlineKeyboardButton(text="🖼 Rasmni o'zgartirish",
                                                      callback_data=f"superadmin:edit_photo:{product[0]}")

                             ],
                             [
                                 InlineKeyboardButton(text="⬅️ Orqaga", callback_data="superadmin:products")
                             ]
                         ]))


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:edit_price", state="*")
async def edit_price(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    product_id = call.data.split(":")[-1]
    await state.update_data(product_id=product_id)
    await call.message.answer("💵 Mahusulot narxini kiriting:")
    await state.set_state(f"edit_price:price")


@dp.message_handler(IsSuperAdmin(), state="edit_price:price")
async def get_price(message: Message, state: FSMContext):
    price = message.text
    data = await state.get_data()
    await db.update_product_price(id=int(data["product_id"]), price=price)
    await message.answer("✅ Mahsulot narxi muvaffaqiyatli o'zgartirildi!", reply_markup=menu_super_admin)
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:edit_desc", state="*")
async def edit_desc(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    product_id = call.data.split(":")[-1]
    await state.update_data(product_id=product_id)
    await call.message.answer("✍️ Mahsulot tavsifini kiriting:")
    await state.set_state(f"edit_desc:desc")


@dp.message_handler(IsSuperAdmin(), state="edit_desc:desc")
async def get_desc(message: Message, state: FSMContext):
    desc = message.text
    data = await state.get_data()
    await db.update_product_desc(id=int(data["product_id"]), desc=desc)
    await message.answer("✅ Mahsulot tavsifi muvaffaqiyatli o'zgartirildi!", reply_markup=menu_super_admin)
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(IsSuperAdmin(), text_contains="superadmin:edit_photo", state="*")
async def edit_photo(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    product_id = call.data.split(":")[-1]
    await state.update_data(product_id=product_id)
    await call.message.answer("🖼 Mahsulot rasmini yuboring:")
    await state.set_state(f"edit_photo:photo")


@dp.message_handler(IsSuperAdmin(), state="edit_photo:photo", content_types=ContentTypes.PHOTO)
async def get_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    data = await state.get_data()
    await db.update_product_photo(id=int(data["product_id"]), file_id=file_id)
    await message.answer("✅ Mahsulot rasmi muvaffaqiyatli o'zgartirildi!", reply_markup=menu_super_admin)
    await state.finish()
    await state.reset_data()