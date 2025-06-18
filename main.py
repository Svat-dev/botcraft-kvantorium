import asyncio
import logging
from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command

from modules.commands import CommandStart, CommandInfo, CommandRegister
from modules.config.config import bot
from modules.config.json import init_json
from modules.constants import EnumCommands, EnumUserRoles
from modules.data import get_main_kb

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

init_json()

@dp.message(Command(EnumCommands.START))
async def cmd_start(msg: types.Message):
    return await CommandStart(msg)

@dp.message(Command(EnumCommands.INFO))
async def cmd_info(msg: types.Message):
    return await CommandInfo(msg)

@dp.message(Command(EnumCommands.REGISTER))
async def cmd_register(msg: types.Message):
    return await CommandRegister(msg, False)

@dp.message(F.text.startswith("пароль:"))
async def cmd_continiue_register(msg: types.Message):
    return await CommandRegister(msg, True)

async def main():
    await dp.start_polling(bot)
    await bot.set_my_commands(commands=get_main_kb(EnumUserRoles.GUEST))

if __name__ == "__main__":
    asyncio.run(main()) 
