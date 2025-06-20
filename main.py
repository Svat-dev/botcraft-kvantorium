import asyncio

from aiogram import types, F
from aiogram.filters.command import Command

from modules.callbacks import (
    CallbackLogout,
    CallbackRegister,
    CallbackCreateEvent,
    CallbackRegisterToEvent,
)
from modules.commands import (
    CommandCreateEvent,
    CommandLogout,
    CommandMyProfile,
    CommandStart,
    CommandInfo,
    CommandRegister,
    CommandGetEvents,
)
from modules.config.config import bot, storage, dp
from modules.config.json import init_json
from modules.constants import EnumCommands, EnumUserRoles, EnumStorageTokens
from modules.data import get_main_kb

init_json()


@dp.message(Command(EnumCommands.START))
async def cmd_start(msg: types.Message):
    return await CommandStart(msg)


@dp.message(Command(EnumCommands.INFO))
async def cmd_info(msg: types.Message):
    return await CommandInfo(msg)


@dp.message(Command(EnumCommands.REGISTER))
async def cmd_register(msg: types.Message):
    return await CommandRegister(msg)


@dp.message(F.text.startswith("ФИО:"))
async def cmd_continue_register(msg: types.Message):
    return await CallbackRegister(msg)


@dp.message(Command(EnumCommands.LOGOUT))
async def cmd_logout(msg: types.Message):
    return await CommandLogout(msg)


@dp.message(F.text.lower().endswith(" аккаунт"))
async def logout_callback_handler(msg: types.Message):
    return await CallbackLogout(msg)


@dp.message(Command(EnumCommands.PROFILE))
async def cmd_get_profile(msg: types.Message):
    return await CommandMyProfile(msg)


@dp.message(Command(EnumCommands.CREATE_EVENT))
async def cmd_create_event(msg: types.Message):
    return await CommandCreateEvent(msg)


@dp.message(F.text.startswith("Ивент "))
async def cmd_create_event(msg: types.Message):
    return await CallbackCreateEvent(msg)


@dp.message(Command(EnumCommands.EVENTS))
async def cmd_get_events(msg: types.Message):
    return await CommandGetEvents(msg)


@dp.callback_query(F.data.split(":")[0] == "register_to_event")
async def register_to_event(callback: types.CallbackQuery):
    return await CallbackRegisterToEvent(callback)


async def main():
    await dp.start_polling(bot)
    await bot.set_my_commands(commands=get_main_kb(EnumUserRoles.GUEST))


if __name__ == "__main__":
    asyncio.run(main())
