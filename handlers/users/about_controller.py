from aiogram import types

from filters import IsUser
from keyboards.inline.userKeyboards import back
from loader import dp


@dp.callback_query_handler(IsUser(), text='user:about', state='*')
async def user_about(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        text=f'🤖 Biz haqimizda'
             f'\n\n♦️ Fariman - INSTANT YEAST'
             f'\n✅ 27 yillik ishonch va sifat'
             f'\n📞 Tel: +998977485555'
             f'\n📌 Instagram: https://www.instagram.com/fariman.uzb/'
             f'\n📧 Telegram: https://t.me/farimanUz'
             f'\n\n👨‍💻 Bot @azodov_001 tomonidan yaratilgan.',
        reply_markup=back
    )
