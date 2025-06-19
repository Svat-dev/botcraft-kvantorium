from aiogram import types

from modules.config.json import (
    create_event,
    get_user_data,
    create_user,
    read_data,
    update_user,
)
from modules.constants import EnumUserRoles, EnumStorageTokens, EnumCommands
from modules.config.config import dp


async def CommandStart(msg: types.Message):
    await msg.answer(
        "Привет, чтобы начать,\nвведи любую команду из предложенных в меню"
    )


async def CommandInfo(msg: types.Message):
    user_id = msg.from_user.id
    creator_user_id = 0

    if user_id == creator_user_id:
        creator_name = "Вы"
    else:
        creator_name = "@swuttik_get"

    await msg.answer('Бот Кванториума "Ивент-мастер"')
    await msg.answer(f"Создатель: {creator_name}")
    await msg.answer("Версия 1.0.0")


async def CommandRegister(msg: types.Message, is_continue: bool):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))
    data = read_data()

    if is_continue:
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

    await dp.storage.set_data(
        str(msg.from_user.id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.REGISTER},
    )
    await msg.reply('Придумайте пароль, запишите его как "рпароль: [ваш пароль]"')


async def CommandLogout(msg: types.Message):
    user = get_user_data(msg.from_user.id)
    if not user:
        return await msg.reply("Вы не в системе, чтобы удалить")

    kb = [
        [
            types.KeyboardButton(text="Удалить аккаунт"),
            types.KeyboardButton(text="Не удалять аккаунт"),
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите вариант"
    )

    await dp.storage.set_data(
        str(msg.from_user.id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.LOGOUT},
    )

    await msg.reply("Вы уверены, что хотите удалить аккаунт?", reply_markup=keyboard)


async def CommandMyProfile(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if not user:
        await msg.reply("Для этого надо авторизоваться!")

    await msg.reply(
        f"ID: {user_id}\nДата создания {user["created_at"].replace("-", " / ")}\nРоль: {user["role"]}\nИвенты:"
    )


async def CommandCreateEvent(msg: types.Message, is_continue: bool):
    user_id = msg.from_user.id
    user = get_user_data(user_id)
    local = await dp.storage.get_data(str(user_id))

    if user["role"] == EnumUserRoles.GUEST and user["role"] == EnumUserRoles.STUDENT:
        return await msg.reply("У вас недостаточно прав!")

    if is_continue:
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

        return await msg.answer("Ивент создан")

    await dp.storage.set_data(
        str(msg.from_user.id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.CREATE_EVENT},
    )
    return await msg.reply(
        "Чтобы создать ивент отправьте сообщение в таком формате:\nИвент - [название]/[описание]/[макс. участников][дата проведения (год|день|месяц)]/[время проведения (часы:минуты)]/[длительность (часы:минуты)]"
    )
