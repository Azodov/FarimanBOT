from aiogram import types

from aiogram.dispatcher.filters import BoundFilter
from loader import db


class IsUser(BoundFilter):
    async def check(self, message: types.Message):
        user_id = int(message.from_user.id)
        user = await db.select_user(telegram_id=user_id)
        if user:
            return True
        else:
            return False


class IsGuest(BoundFilter):
    async def check(self, message: types.Message):

        user_id = int(message.from_user.id)
        user = await db.select_user(telegram_id=user_id)

        if not user:
            return True
        else:
            return False
