from aiogram import types

from modules.config.json import remove_user, create_user
from modules.config.config import dp
from modules.constants import EnumStorageTokens, EnumCommands


async def CallbackLogout(msg: types.Message):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))
    logout_txt = msg.text.lower()

    if local[EnumStorageTokens.COMMAND_IN_ACTION] != EnumCommands.LOGOUT or not local:
        return False

    if logout_txt == "удалить аккаунт":
        await msg.reply("Вы удалили аккаунт")
        remove_user(user_id)
    elif logout_txt == "не удалять аккаунт":
        await msg.reply("Хорошо")

    return await dp.storage.update_data(
        str(user_id), {f"{EnumStorageTokens.COMMAND_IN_ACTION}": None}
    )


async def CallbackRegister(msg: types.Message):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))
    data = read_data()

    if local[EnumStorageTokens.COMMAND_IN_ACTION] != EnumCommands.REGISTER:
        return False

    if str(user_id) in data["users"]:
        return await msg.reply("Такой пользователь уже существует")

    password = msg.text.split(" ")[1]
    create_user(user_id, password, EnumUserRoles.MENTOR)

    await msg.reply("Аккаунт успешно создан!")
    return await dp.storage.update_data(
        str(user_id), {f"{EnumStorageTokens.COMMAND_IN_ACTION}": None}
    )


async def CallbackCreateEvent(msg: types.Message):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))

    if local[EnumStorageTokens.COMMAND_IN_ACTION] != EnumCommands.CREATE_EVENT:
        return False

    event_info = msg.text.split(" - ")[1].split("/")
    title = event_info[0]
    desc = event_info[1]
    limit = int(event_info[2])
    date = event_info[3].split("|")
    time = event_info[4]
    duration = event_info[5]

    create_event(
        f"{date[0]}.{date[2]}.{date[1]} / {time}", limit, duration, desc, title
    )

    await dp.storage.update_data(
        str(user_id), {f"{EnumStorageTokens.COMMAND_IN_ACTION}": None}
    )

    return await msg.answer("Ивент успешно создан!")


async def CallbackRegisterToEvent(callback: types.CallbackQuery):
    user_id = await dp.storage.get_data(EnumStorageTokens.USER_ID)
    event_id = callback.data.split(":")[1]
    msg = callback.message

    await msg.answer(event_id, user_id)
