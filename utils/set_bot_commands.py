from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Start to use the bot🚀"),
            types.BotCommand(command="help", description="Help🙏"),
            types.BotCommand(command="feedback", description="Send feedback to admin✍️")
        ]
    )
