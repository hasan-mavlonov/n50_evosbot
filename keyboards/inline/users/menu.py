from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton("Burgers"),
        KeyboardButton("Shawarma")
    )
    markup.row(
        KeyboardButton("Salads, Bread, and Sides"),
        KeyboardButton("Hot Dogs")
    )
    markup.row(
        KeyboardButton("Sauces and Additions"),
        KeyboardButton("Desserts")
    )
    markup.row(
        KeyboardButton("Cold Drinks"),
        KeyboardButton("Hot Drinks")
    )
    markup.row(
        KeyboardButton("Combo Meals"),
        KeyboardButton("⬅️ Back to Main Menu")
    )
    markup.row(
        KeyboardButton("🛒Cart")  # Assuming this is the 'Корзина' button
    )
    return markup
