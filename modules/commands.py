from aiogram import types

from modules.config.json import get_user_data, create_user, read_data, update_user
from modules.constants import EnumUserRoles


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
    data = read_data()

    if is_continue and str(user_id) not in data["users"]:
        password = msg.text.split(" ")[1]
        create_user(user_id, password, EnumUserRoles.STUDENT)
        return await msg.reply("Аккаунт успешно создан!")


    if str(user_id) in data["users"]:
        await msg.reply("Такой пользователь уже существует")
    else:
        await msg.reply('Придумайте пароль, запишите его как "рпароль: [ваш пароль]"')

async def CommandLogout(msg: types.Message):
    user = get_user_data(msg.from_user.id)
    if not user:
        return await msg.reply("Вы не в системе, чтобы удалить")

    kb = [
        [
            types.KeyboardButton(text="Удалить аккаунт"),
            types.KeyboardButton(text="Не удалять аккаунт")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите вариант"
    )

    await msg.reply("Вы уверены, что хотите удалить аккаунт?", reply_markup=keyboard)

async def CommandMyProfile(msg: types.Message):
    user_id = msg.from_user.id
    user = get_user_data(user_id)

    if not user:
        await msg.reply("Для этого надо авторизоваться!")

    await msg.reply(f"ID: {user_id}\nДата создания {user["created_at"].replace("-", " / ")}\nИвенты:")

