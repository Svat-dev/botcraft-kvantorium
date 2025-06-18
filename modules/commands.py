from aiogram import types
from modules.config.json import get_user_data, create_user
from modules.constants import EnumUserRoles

async def CommandStart(msg: types.Message):
    await msg.answer("Привет, чтобы начать,\nвведи любую команду из предложенных в меню")

async def CommandInfo(msg: types.Message):
    user_id = msg.from_user.id
    creator_user_id = 0

    if user_id == creator_user_id:
        creator_name = "Вы"
    else:
        creator_name = "@swuttik_get"
    
    await msg.answer("Бот Кванториума \"Ивент-мастер\"")
    await msg.answer(f"Создатель: {creator_name}")
    await msg.answer("Версия 1.0.0")

async def CommandRegister(msg: types.Message, is_continiue: bool):
    user_id = msg.from_user.id

    if is_continiue:
        password = msg.text.split(" ")[1]
        create_user(user_id, password, EnumUserRoles.STUDENT)
        await msg.reply("Аккаунт успешно создан!")

    data = get_user_data(user_id)

    if data:
        await msg.reply("Такой пользователь уже существует")
    else:
        await msg.reply("Придумайте пароль, запишите его как \"пароль: [ваш пароль]\"")