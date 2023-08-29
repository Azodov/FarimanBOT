from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Mahsulotlar", callback_data="user:products"),
        ],
        [
            InlineKeyboardButton(text="🛒 Savatcha", callback_data="user:cart"),
        ],
        [
            InlineKeyboardButton(text="🤖 Bot haqida", callback_data="user:about")
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user:cancel")
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

done = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Bajarildi", callback_data="user:done")
        ]
    ]
)

cart = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Davom etish", callback_data="user:products")
        ],
        [
            InlineKeyboardButton(text="🛍 Savatchaga o'tish", callback_data="user:cart")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

cart_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 Buyurtmani tasdiqlash", callback_data="user:pay")
        ],
        [
            InlineKeyboardButton(text="🗑 Savatni bo'shatish", callback_data="user:delete_cart")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

payment_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 Karta orqali", callback_data="user:payment:card"),
            InlineKeyboardButton(text="💵 Naqd pul", callback_data="user:payment:cash")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="user:cancel")
        ]
    ]
)

