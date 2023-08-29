from aiogram.types import CallbackQuery

from filters import IsSuperAdmin
from loader import dp


@dp.callback_query_handler(IsSuperAdmin(), text="superadmin:stat", state="*")
async def show_stat(call: CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.answer("ishladi")
