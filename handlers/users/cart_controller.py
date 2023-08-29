from aiogram import types

from filters import IsUser
from keyboards.inline.userKeyboards import cart, cart_product, back
from loader import dp, db


@dp.callback_query_handler(IsUser(), text="user:cart")
async def show_cart(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    user_id = call.from_user.id
    products_into_cart = await db.select_user_cart(user_id=user_id, isPaid='SELECTED')
    need_to_pay = 0
    products_count = len(products_into_cart)
    products = []
    if cart:
        for product in products_into_cart:
            need_to_pay += (int(product["price"]) * int(product["count"]))
            products.append(
                f"📦 {product['name']} {product['massa']} - {product['count']} x {int(product['price'])}"
                f" = {int(product['price']) * int(product['count'])} so'm\n")
        try:
            if need_to_pay == 0:
                await call.message.edit_text("🤷‍♂️ Sizning savatchangiz bo'sh", reply_markup=back)
                return
            await call.message.edit_text(f"🛒 Sizning savatchangiz:\n\n"
                                         f"📦 Ja'mi mahsulotlar turi: {products_count} dona\n"
                                         f"💰 Umumiy summa: {need_to_pay} so'm\n\n"
                                         f"📦 Mahsulotlar:\n"
                                         f"{''.join(products)}",
                                         reply_markup=cart_product)
        except:
            await call.message.delete()
            await call.message.answer(f"🛒 Sizning savatchangiz:\n\n"
                                      f"📦 Ja'mi mahsulotlar turi: {products_count} dona\n"
                                      f"💰 Summa: {need_to_pay} so'm\n\n"
                                      f"📦 Mahsulotlar:\n"
                                      f"{''.join(products)}",
                                      reply_markup=cart_product)
    else:
        await call.message.answer("🤷‍♂️ Sizning savatchangiz bo'sh", reply_markup=back)
        return


@dp.callback_query_handler(IsUser(), text="user:delete_cart", state="*")
async def delete_products_from_cart(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    user_id = call.from_user.id
    await db.delete_user_cart(user_id=user_id, isPaid='SELECTED')
    await call.message.edit_text("🤷‍♂️ Sizning savatchangiz bo'sh", reply_markup=cart)
