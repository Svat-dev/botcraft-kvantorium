from aiogram import types

from modules.config.json import (
    get_user_data,
    get_events_data,
    get_event,
)
from modules.constants import EnumUserRoles, EnumStorageTokens, EnumCommands
from modules.config.config import dp
from modules.data import get_events_inline_kb


async def CommandStart(msg: types.Message):
    user_id = msg.from_user.id

    await dp.storage.set_data(
        str(user_id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.START},
    )

    await dp.storage.set_data(f"{EnumStorageTokens.USER_ID}", {"data": str(user_id)})

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


async def CommandRegister(msg: types.Message):
    user_id = msg.from_user.id

    await dp.storage.set_data(
        str(user_id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.REGISTER},
    )

    await msg.reply('Напишите свое ФИО в таком формате "ФИО: [фамилия] [имя]"')


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
        return await msg.reply("Для этого надо авторизоваться!")

    event_names = []

    for id in user["events"]:
        event = get_event(id)
        event_names.append(event["title"])

    if not event_names:
        events = "Нет ивентов"
    else:
        events = ", ".join(event_names)

    await msg.reply(
        f"ID: {user_id}\nДата создания {user["created_at"].replace("-", " / ")}\nРоль: {user["role"]}\nИвенты: {events}\n"
    )


async def CommandCreateEvent(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if user["role"] == EnumUserRoles.GUEST and user["role"] == EnumUserRoles.STUDENT:
        return await msg.reply("У вас недостаточно прав!")

    await dp.storage.set_data(
        str(msg.from_user.id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.CREATE_EVENT},
    )
    return await msg.reply(
        "Чтобы создать ивент отправьте сообщение в таком формате:\nИвент - [название]/[описание]/[макс. участников][дата проведения (год|день|месяц)]/[время проведения (часы:минуты)]/[длительность (часы:минуты)]"
    )


async def CommandGetEvents(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if user["role"] == EnumUserRoles.GUEST:
        return await msg.reply("У вас недостаточно прав!")

    events = get_events_data().items()
    await msg.reply("Все доступные ивенты:")

    for id, event in events:
        date = event["date"].split(" / ")[0]
        time_start = event["date"].split(" / ")[1]
        hours = int(time_start.split(":")[0]) + int(event["duration"].split(":")[0])
        mins = int(time_start.split(":")[1]) + int(event["duration"].split(":")[1])
        time_end = f"{hours}:{mins}"

        await msg.answer(
            text=f"{event['title']}\n{event["desc"]}\nДата: {date} {time_start} - {time_end}\nМакс. участников: {event["participants_limit"]}",
            reply_markup=get_events_inline_kb(id).as_markup(),
        )
