from aiogram import Dispatcher

from loader import dp
from .admin_filter import IsSuperAdmin, IsAdmin
from .user_filter import IsUser, IsGuest

if __name__ == "filters":
    dp.filters_factory.bind(IsSuperAdmin)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsUser)
    dp.filters_factory.bind(IsGuest)
