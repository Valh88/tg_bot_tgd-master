from aiogram import Bot
from aiogram.types import BotCommand
from ..lexicon.lexicon import COMMANDS


async def main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)
