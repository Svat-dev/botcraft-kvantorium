from aiogram import types

from modules.config.json import remove_user
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
