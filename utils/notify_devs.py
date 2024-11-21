from loader import bot
from logging_settings import logger
from main.config import DEVS


async def send_notification_to_devs(dispatcher):
    try:
        for dev in DEVS:
            await bot.send_message(text="Bot started working", chat_id=dev, )
    except Exception as e:
        logger.error(f"While sending to devs encountered this error: {e}")
