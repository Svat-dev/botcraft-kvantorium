import asyncio
import re

from aiogram import types, F
from aiogram.filters.command import Command

from modules.callbacks import (
    CallbackLogout,
    CallbackRegister,
    CallbackCreateEvent,
    CallbackRegisterToEvent,
    CallbackAddMentor,
    CallbackAddProjectsMentor,
)
from modules.commands import (
    CommandAddMentor,
    CommandAskToMentor,
    CommandCancel,
    CommandCreateEvent,
    CommandGetActiveEvents,
    CommandGetMentors,
    CommandLogout,
    CommandMyProfile,
    CommandStart,
    CommandInfo,
    CommandRegister,
    CommandGetEvents,
    CommandAddProjectsMentor,
)
from modules.config.config import bot, dp
from modules.config.json import init_json
from modules.constants import EnumCommands, EnumUserRoles
from modules.data import get_main_kb

init_json()


@dp.message(Command(EnumCommands.START))
async def cmd_start(msg: types.Message):
    return await CommandStart(msg)


@dp.message(Command(EnumCommands.CANCEL))
async def cmd_start(msg: types.Message):
    return await CommandCancel(msg)


@dp.message(Command(EnumCommands.INFO))
async def cmd_info(msg: types.Message):
    return await CommandInfo(msg)


@dp.message(Command(EnumCommands.REGISTER))
async def cmd_register(msg: types.Message):
    return await CommandRegister(msg)


@dp.message(F.text.lower().startswith("фио:"))
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


@dp.message(Command(EnumCommands.ACTIVE_EVENTS))
async def cmd_get_active_events(msg: types.Message):
    return await CommandGetActiveEvents(msg)


@dp.callback_query(F.data.split(":")[0] == "register_to_event")
async def register_to_event(callback: types.CallbackQuery):
    return await CallbackRegisterToEvent(callback)


@dp.message(Command(EnumCommands.ADD_MENTOR))
async def cmd_add_new_mentor(msg: types.Message):
    return await CommandAddMentor(msg)


@dp.message(Command(EnumCommands.ADD_MENTOR_TO_PROJECT))
async def cmd_add_mentor_to_project(msg: types.Message):
    return await CommandAddProjectsMentor(msg)


@dp.message(F.text.lower().startswith("добавить преподавателя:"))
async def callback_add_mentor_to_project(msg: types.Message):
    return await CallbackAddProjectsMentor(msg)


@dp.message(F.text.lower().startswith("фио преподавателя:"))
async def callback_add_new_mentor(msg: types.Message):
    return await CallbackAddMentor(msg)


@dp.message(Command(EnumCommands.GET_MENTORS))
async def cmd_get_mentors(msg: types.Message):
    return await CommandGetMentors(msg)


@dp.message(F.text.startswith(f"/{EnumCommands.ASK}"))
async def cmd_ask(msg: types.Message):
    return await CommandAskToMentor(msg)


async def main():
    await dp.start_polling(bot)
    await bot.set_my_commands(commands=get_main_kb(EnumUserRoles.GUEST))


if __name__ == "__main__":
    asyncio.run(main())
