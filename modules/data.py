from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.constants import EnumUserRoles, EnumCommands


def get_main_kb(role: EnumUserRoles) -> list[types.BotCommand]:
    if role == EnumUserRoles.GUEST:
        return [
            types.BotCommand(
                command=EnumCommands.START, description="Перезапустить бота"
            ),
            types.BotCommand(command=EnumCommands.INFO, description="О боте"),
            types.BotCommand(command=EnumCommands.LOGIN, description="Войти"),
            types.BotCommand(
                command=EnumCommands.REGISTER, description="Зарегистрироваться"
            ),
        ]
    elif role == EnumUserRoles.STUDENT:
        return [
            types.BotCommand(
                command=EnumCommands.START, description="Перезапустить бота"
            ),
            types.BotCommand(command=EnumCommands.INFO, description="О боте"),
            types.BotCommand(command=EnumCommands.LOGOUT, description="Выйти"),
            types.BotCommand(command=EnumCommands.EVENTS, description="Все события"),
            types.BotCommand(command=EnumCommands.MY_EVENTS, description="Мои события"),
            types.BotCommand(
                command=EnumCommands.ASK, description="Спросить у куратора"
            ),
            types.BotCommand(
                command=EnumCommands.VOTE_PROJECT, description="Проголосовать за проект"
            ),
        ]
    elif role == EnumUserRoles.MENTOR:
        return [
            types.BotCommand(
                command=EnumCommands.START, description="Перезапустить бота"
            ),
            types.BotCommand(command=EnumCommands.INFO, description="О боте"),
            types.BotCommand(command=EnumCommands.LOGOUT, description="Выйти"),
            types.BotCommand(command=EnumCommands.EVENTS, description="Все события"),
            types.BotCommand(command=EnumCommands.MY_EVENTS, description="Мои события"),
        ]
    elif role == EnumUserRoles.MODER:
        return [
            types.BotCommand(
                command=EnumCommands.START, description="Перезапустить бота"
            ),
            types.BotCommand(command=EnumCommands.INFO, description="О боте"),
            types.BotCommand(command=EnumCommands.LOGOUT, description="Выйти"),
            types.BotCommand(command=EnumCommands.EVENTS, description="Все события"),
        ]
    elif role == EnumUserRoles.ADMIN:
        return [
            types.BotCommand(
                command=EnumCommands.START, description="Перезапустить бота"
            ),
            types.BotCommand(command=EnumCommands.INFO, description="О боте"),
            types.BotCommand(command=EnumCommands.LOGOUT, description="Выйти"),
            types.BotCommand(command=EnumCommands.EVENTS, description="Все события"),
        ]


def get_events_inline_kb(event_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text="Зарегистрироваться",
            callback_data=f"register_to_event:{event_id}",
        ),
    )

    return builder
