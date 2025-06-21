from aiogram import types

from modules.config.json import (
    get_event_by_name,
    get_question,
    get_user_by_name,
    remove_user,
    create_user,
    get_user_data,
    update_event,
    update_user,
    get_event,
    read_data,
    create_event
)
from modules.config.config import dp
from modules.constants import EnumStorageTokens, EnumCommands, EnumUserRoles


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

    name = msg.text.split(":")[1]
    create_user(user_id, name, EnumUserRoles.STUDENT)

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
    local = await dp.storage.get_data(EnumStorageTokens.USER_ID)
    msg = callback.message

    user_id = local["data"]
    user = get_user_data(user_id)

    if user["role"] != EnumUserRoles.STUDENT:
        return await msg.answer("Вы не студент")

    event_id = callback.data.split(":")[1]
    event = get_event(event_id)

    if event_id in user["events"]:
        return await msg.answer("Вы уже зарегистрированы на этот ивент")

    update_event(event_id, "participants", {str(user): {}})
    update_user(user_id, "events", {event_id: {}})
    await msg.answer(f'Вы успешно зарегистрировались на ивент "{event["title"]}"!')


async def CallbackAddMentor(msg: types.Message):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))

    if local[EnumStorageTokens.COMMAND_IN_ACTION] != EnumCommands.ADD_MENTOR:
        return False

    msg_data = msg.text.split(":")[1]
    last_name = msg_data.split()[0]
    first_name = msg_data.split()[1]

    user = get_user_by_name(first_name, last_name)
    user_role = user.get("user")["role"]

    if not user.get("user"):
        return await msg.reply("Такого пользваотеля нет")
    elif user_role == EnumUserRoles.ADMIN or user_role == EnumUserRoles.MODER:
        return await msg.reply("Этого пользователя добавить в наставники нельзя")
    elif user_role == EnumUserRoles.MENTOR:
        return await msg.reply("Этот пользовательуже наставник")

    update_user(user.get("id"), "role", EnumUserRoles.MENTOR)

    return await msg.reply("Наставник успешно добавлен!")


async def CallbackAddProjectsMentor(msg: types.Message):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))

    if local[EnumStorageTokens.COMMAND_IN_ACTION] != EnumCommands.ADD_MENTOR_TO_PROJECT:
        return False
    
    msg_data = msg.text.split(":")[1]
    event_name = msg_data.split("-")[0]
    last_name = msg_data.split("-")[1]
    first_name = msg_data.split("-")[2]

    user = get_user_by_name(first_name, last_name)
    user_role = user.get("user")["role"]

    if not user.get("user"):
        return await msg.reply("Такого пользователя нет")
    
    if user_role == EnumUserRoles.MENTOR:
        event = get_event_by_name(event_name)

        if not event.get("event"):
            return await msg.reply("Такого ивента нет")

        update_event(event.get("id"), "mentor_id", user.get("id"))
        update_user(user.get("id"), "events", {event.get("id"): {}})

        return await msg.reply("Наставник успешно добавлен в проект")
    else:
        return await msg.reply("Этот пользователь не является преподавателем")


async def CallbackAnswer(callback: types.CallbackQuery):
    question_id = callback.data.split(":")[1]
    user_id = await dp.storage.get_data(EnumStorageTokens.USER_ID)

    await callback.message.reply("Отправьте ответ на вопрос - /answer : [ответ]")

    await dp.storage.set_data(
        str(user_id),
        {f"{EnumStorageTokens.QUESTION_ID}": question_id}
    )

    return await dp.storage.set_data(
        str(user_id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.REGISTER}
    )
