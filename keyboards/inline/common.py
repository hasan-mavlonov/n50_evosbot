from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🍴Menu")
            ],
            [
                KeyboardButton(text="🛒Cart")
            ],
            [
                KeyboardButton(text="✍️ Leave Feedback"),
                KeyboardButton(text="⚙️Settings")
            ]
        ]
    )
    return markup


async def location_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("📍 Send Location", request_location=True),
        KeyboardButton("⬅️ Back to Main Menu")
    )
    return markup


async def confirmation_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("✅ Confirm"),
        KeyboardButton("❌ Cancel")
    )
    return markup


languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Uzbek", callback_data="uz"),
            InlineKeyboardButton(text="Russian", callback_data="ru"),
            InlineKeyboardButton(text="English", callback_data="en"),
        ]
    ]
)
