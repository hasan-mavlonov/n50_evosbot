from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.inline.users.menu import menu_keyboard
from loader import dp

user_cart = {}


@dp.message_handler(
    text=["Burgers", "Shawarma", "Salads, Bread, and Sides", "Hot Dogs", "Sauces and Additions", "Desserts",
          "Cold Drinks", "Hot Drinks", "Combo Meals"])
async def product_selection(message: types.Message):
    product_name = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("✅ Yes, add to cart"),
        KeyboardButton("❌ No, cancel")
    )

    # Ask user for confirmation to add the selected product to cart
    await message.answer(f"Do you want to add '{product_name}' to your cart?", reply_markup=markup)

    # Store the selected product for later confirmation
    if user_cart.get(message.from_user.id) is None:
        user_cart[message.from_user.id] = []  # Initialize the user's cart as an empty list
    user_cart[message.from_user.id].append({'product': product_name, 'action': 'pending'})


@dp.message_handler(text=["✅ Yes, add to cart", "❌ No, cancel"])
async def confirm_add_to_cart(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_cart and user_cart[user_id]:  # Ensure there are items in the cart
        last_added_item = user_cart[user_id][-1]  # Get the last added item for confirmation
        product = last_added_item['product']

        if message.text == "✅ Yes, add to cart":
            # Add product to the user's cart
            user_cart[user_id].append({'product': product, 'action': 'added'})
            await message.answer(f"'{product}' has been added to your cart.", reply_markup=await menu_keyboard())
        else:
            await message.answer(f"Cancelled adding '{product}' to your cart.", reply_markup=await menu_keyboard())

        # Remove the pending action after confirmation
        user_cart[user_id] = [item for item in user_cart[user_id] if item['action'] != 'pending']
    else:
        # This condition ensures that the handler won't execute unless there's a pending action
        await message.answer("Something went wrong. Please select a product first.", reply_markup=await menu_keyboard())


@dp.message_handler(text=["🛒Cart"])
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🛒 Buy Now"),
        KeyboardButton("⬅️ Back to Menu")
    )

    if user_id in user_cart and user_cart[user_id]:  # Check if the user has items in the cart
        cart_items = [item['product'] for item in user_cart[user_id] if item['action'] == 'added']
        if cart_items:
            # Format the cart items into a list
            cart_message = "🛒 Your Cart:\n" + "\n".join([f"- {item}" for item in cart_items])
        else:
            cart_message = "🛒 Your cart is empty."
    else:
        cart_message = "🛒 Your cart is empty."

    await message.answer(cart_message, reply_markup=markup)


@dp.message_handler(text=["🛒 Buy Now"])
async def buy_now_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_cart and any(item['action'] == 'added' for item in user_cart[user_id]):
        # Process the order
        cart_items = [item['product'] for item in user_cart[user_id] if item['action'] == 'added']
        order_summary = "\n".join([f"- {item}" for item in cart_items])

        await message.answer(
            f"✅ Thank you for your order! Here is what you ordered:\n{order_summary}\n\nYour cart has been emptied.",
            reply_markup=await menu_keyboard()
        )

        # Empty the user's cart
        user_cart[user_id] = []
    else:
        await message.answer("🛒 Your cart is empty. Add items to your cart before placing an order.",
                             reply_markup=await menu_keyboard())
