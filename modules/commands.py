from aiogram import types

from datetime import datetime

from modules.config.json import (
    create_question,
    get_event_by_name,
    get_user_data,
    get_events_data,
    get_event,
    get_users,
)
from modules.constants import EnumUserRoles, EnumStorageTokens, EnumCommands
from modules.config.config import dp, bot
from modules.data import get_answer_question_inline_kb, get_events_inline_kb


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

        time_end = (
            f"{hours if hours > 9 else f"0{hours}"}:{mins if mins > 9 else f"0{mins}"}"
        )

        mentor_id = event["mentor_id"]
        participants_count: int = 0

        if not mentor_id:
            mentor_name = "Нет наставника"
        else:
            mentor = get_user_data(int(mentor_id))
            mentor_name = f"{mentor.get("last_name")} {mentor.get("first_name")}"

        for _ in event["participants"].values():
            participants_count += 1

        if participants_count == 0:
            participants = f"Макс. участников: {event["participants_limit"]}"
        elif participants_count == int(event["participants_limit"]):
            participants = f"Мест больше нет"
        else:
            participants = (
                f"Участники: {participants_count}/{event["participants_limit"]}"
            )

        await msg.answer(
            text=f"{event['title']}\n{event["desc"]}\nДата: {date} {time_start} - {time_end}\n{participants}\nНаставник: {mentor_name}",
            reply_markup=get_events_inline_kb(id).as_markup(),
        )


async def CommandGetActiveEvents(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id=user_id)

    if user["role"] == EnumUserRoles.GUEST:
        return await msg.reply(text="Вам необходимо авторизоваться")

    events = get_events_data()
    index: int = 1

    await msg.reply("Текущие мероприятия:")

    for id, event in events.items():
        date = event["date"].split("/")[0].replace(" ", "")
        date_str = event["date"].replace(" ", "")

        time_start = event["date"].split("/")[1].replace(" ", "").split(":")
        time_end = event["duration"].split(":")

        hours = int(time_start[0]) + int(time_end[0])
        mins = int(time_start[1]) + int(time_end[1])

        total_hours = (mins // 60) + hours
        total_mins = mins - 60 if (mins % 60) > 0 else mins

        time = f"{total_hours if total_hours > 9 else f"0{total_hours}"}:{total_mins if total_mins > 9 else f"0{total_mins}"}"

        date_start = datetime.strptime(date_str, "%Y.%m.%d/%H:%M")
        date_end = datetime.strptime(f"{date}/{time}", "%Y.%m.%d/%H:%M")
        date_current = datetime(year=1900, month=1, day=1).today()

        if date_start < date_current and date_end > date_current:
            await msg.answer(f"{index}. {event["title"]}\n\tВремя окончания: {time}")
            index += 1

    if index == 1:
        return await msg.answer("Сейчас нет активных мероприятий")


async def CommandAddProjectsMentor(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if user["role"] != EnumUserRoles.ADMIN and user["role"] != EnumUserRoles.MODER:
        return await msg.reply("У вас недостаточно прав!")

    await dp.storage.set_data(
        str(msg.from_user.id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.ADD_MENTOR_TO_PROJECT},
    )

    return await msg.reply(
        "Отправьте мне ФИ преподавателя и название ивента\nвот так - Добавить преподавателя: [название ивента]-[фамилия]-[имя]"
    )


async def CommandAddMentor(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if user["role"] != EnumUserRoles.ADMIN and user["role"] != EnumUserRoles.MODER:
        return await msg.reply("У вас недостаточно прав!")

    await dp.storage.set_data(
        str(msg.from_user.id),
        {f"{EnumStorageTokens.COMMAND_IN_ACTION}": EnumCommands.ADD_MENTOR},
    )

    return await msg.reply(
        "Отправьте мне ФИ преподавателя\nвот так - ФИО преподавателя: [фамилия] [имя]"
    )


async def CommandCancel(msg: types.Message):
    user_id = msg.from_user.id
    local = await dp.storage.get_data(str(user_id))

    if local[EnumStorageTokens.COMMAND_IN_ACTION] != EnumCommands.START:
        await msg.reply("Вы отменили действие")
        return await dp.storage.set_data(
            str(user_id), {f"{EnumStorageTokens.COMMAND_IN_ACTION}": None}
        )
    else:
        return False


async def CommandGetMentors(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    users = get_users()
    index = 1
    text: str = ""

    if user["role"] != EnumUserRoles.ADMIN and user["role"] != EnumUserRoles.MODER:
        return await msg.reply("У вас недостаточно прав!")

    for id, data in users.items():
        if data["role"] == EnumUserRoles.MENTOR:
            _user = data
            text = f"{index}. {_user["last_name"]} {_user["first_name"]}"
            index += 1

    await msg.reply("Вот все преподаватели:")
    return await msg.answer(text)


async def CommandAskToMentor(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if user["role"] != EnumUserRoles.STUDENT and user["role"] != EnumUserRoles.ADMIN:
        return await msg.reply(
            text="Вопрос могут отправлять только ученики и участники ивента"
        )

    content = msg.text.split(f"/{EnumCommands.ASK} ")
    content_length = len(content)

    if content_length != 2:
        return await msg.reply(
            "Вопрос необходимо задать в таком формате:\n/ask [название ивента] | [вопрос]"
        )

    content_2 = content[1].split("|")
    content_2_length = len(content_2)

    if content_2_length != 2:
        return await msg.reply(
            "Вопрос необходимо задать в таком формате:\n/ask [название ивента] | [вопрос]"
        )

    event_name = content_2[0]

    if not event_name:
        return await msg.reply(
            "Вопрос необходимо задать в таком формате:\n/ask [название ивента] | [вопрос]"
        )

    event = get_event_by_name(event_name)

    if not event.get("event"):
        return await msg.reply("Мероприятие не найдено")

    mentor_id = event.get("event")["mentor_id"]

    if not mentor_id:
        return await msg.reply("Нет наставника для этого мероприятия")

    mentor = get_user_data(user_id=mentor_id)
    message = content[1].split("|")[1]

    question_id = create_question(user_id, mentor_id, event.get("id"), message)

    builder = get_answer_question_inline_kb(question_id)

    await bot.send_message(
        int(mentor_id),
        f'Вы получили вопрос от участника события "{event.get("event")["title"]}".\nТекст: {message}',
        reply_markup=builder.as_markup(),
    )

    return await msg.reply(
        f'Ваш вопрос по событию "{event.get("event")["title"]}" отправлен преподавателю {mentor["last_name"]} {mentor["first_name"]}'
    )
