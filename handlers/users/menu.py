from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

from keyboards.inline.common import start_keyboard
from keyboards.inline.users.menu import menu_keyboard
from loader import dp, bot
from logging_settings import logger
from main.config import ADMINS


@dp.message_handler(commands="feedback")
async def send_feedback_to_admins(message: types.Message):
    text = "Enter your feedback:"
    await message.reply(text=text)

    @dp.message_handler()
    async def feedback_handler(feedback_message: types.Message):
        feedback = feedback_message.text
        await message.answer(text="Thank you your feedback was sent to admins!", reply_markup=await start_keyboard())

        for admin in ADMINS:
            try:
                await bot.send_message(text=
                                       f"Here is your feedback from {feedback_message.from_user.first_name}/(@{feedback_message.from_user.username}:    {feedback}",
                                       chat_id=admin)
            except Exception as e:
                logger.error(e)
