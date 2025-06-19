from aiogram import types

from modules.config.json import remove_user

async def CallbackLogout(msg: types.Message):
    is_logout = msg.text.lower()
    user_id = msg.from_user.id

    if is_logout == "удалить аккаунт":
        await msg.reply("Вы удалили аккаунт")
        remove_user(user_id)
    elif is_logout == "не удалять аккаунт":
        await msg.reply("Хорошо")