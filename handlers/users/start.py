from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from keyboards.inline.common import start_keyboard, location_keyboard, confirmation_keyboard, languages
from keyboards.inline.users.menu import menu_keyboard
from loader import dp, bot, _, i18n
from main.config import ADMINS
from logging_settings import logger
from states.user import RegisterState
from utils.get_location_name import get_location_name


@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message):
    text = _("Choose a language")
    await message.answer(text=text, reply_markup=languages)
    await RegisterState.language.set()


@dp.callback_query_handler(state=RegisterState.language)
async def language_handler(call: types.CallbackQuery, state: FSMContext):
    language = call.data  # Assuming the language callback data is "uz", "ru", or "en"

    i18n.ctx_locale.set(language)

    await state.update_data(language=language)
    text = _("Please enter your full name:")
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def full_name_handler(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)

    # Ensure the language context is set before sending the message
    user_data = await state.get_data()
    language = user_data.get("language", "en")  # Default to 'en' if no language is set
    i18n.ctx_locale.set(language)

    # Use translation middleware for dynamic locale
    text = _("Thank you, {full_name}! What would you like to do next?").format(full_name=full_name)
    await message.answer(text=text, reply_markup=await start_keyboard())

    await state.finish()


@dp.message_handler(Text(equals=_("✍️ Leave Feedback")))
async def send_feedback_to_admins(message: types.Message):
    text = _("Enter your feedback:")
    await message.reply(text=text)

    @dp.message_handler()
    async def feedback_handler(feedback_message: types.Message):
        feedback = feedback_message.text
        await message.answer(text=_("Thank you! Your feedback was sent to admins!"),
                             reply_markup=await start_keyboard())

        for admin in ADMINS:
            try:
                await bot.send_message(
                    chat_id=admin,
                    text=_("Here is your feedback from {user}: {feedback}").format(
                        user=f"{feedback_message.from_user.first_name} (@{feedback_message.from_user.username})",
                        feedback=feedback,
                    )
                )
            except Exception as e:
                logger.error(e)


@dp.message_handler(Text(equals=_("🍴Menu")))
async def menu_handler(message: types.Message):
    text = _("Please share your location to see nearby menus:")
    await message.answer(text=text, reply_markup=await location_keyboard())


@dp.message_handler(Text(equals=_("⬅️ Back to Main Menu")))
async def back_to_main_menu(message: types.Message):
    text = _("Choose one of the options")
    await message.answer(text=text, reply_markup=await start_keyboard())


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    user_location = message.location
    if user_location:
        latitude = user_location.latitude
        longitude = user_location.longitude
        location_name = await get_location_name(latitude, longitude)

        text = _("We detected your location as:\n\n📍 *{location_name}*\n\nDo you confirm this location?").format(
            location_name=location_name
        )
        await message.answer(
            text=text,
            reply_markup=await confirmation_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            text=_("Failed to retrieve location. Please try again."),
            reply_markup=await location_keyboard()
        )


@dp.message_handler(Text(equals=_("✅ Confirm")))
async def confirm_location(message: types.Message):
    await message.answer(
        _("Thank you! Your location has been confirmed. You can now proceed with the menu."),
        reply_markup=await menu_keyboard()
    )
