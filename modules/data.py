from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.constants import EnumUserRoles, EnumCommands


def get_user_rights(role: EnumUserRoles) -> dict:
    common_rights = {
        EnumCommands.START: "Перезапустить бота",
        EnumCommands.INFO: "Информация о боте",
        EnumCommands.CANCEL: "Отменить дейтсвие (только текущее)",
        EnumCommands.HELP: "Помощь с командами",
    }

    authed_user_rights = common_rights | {
        EnumCommands.ACTIVE_EVENTS: "Просмотр активных событий",
        EnumCommands.EVENTS: "Просмотр всех доступных событий",
    }

    student_rights = {
        EnumCommands.LOGOUT: "Удалить аккаунт",
        EnumCommands.ASK: "Спросить у наставника проекта",
    }

    mentor_rights = {
        EnumCommands.LOGOUT: "Удалить аккаунт",
        EnumCommands.ANSWER_QUESTION: "Ответить на вопросы участников"
    }

    moder_rights = {
        EnumCommands.LOGOUT: "Удалить аккаунт",
        EnumCommands.ADD_MENTOR: "Добавить нового преподавателя",
        EnumCommands.ADD_MENTOR_TO_PROJECT: "Добавить наставника в событие",
        EnumCommands.CREATE_EVENT: "Создать событие"
    }

    admin_rights = {
        EnumCommands.ADD_MODER: "Добавить нового модератора",
        EnumCommands.ADD_MENTOR_TO_PROJECT: "Добавить наставника в событие",
        EnumCommands.CREATE_EVENT: "Создать событие"
    }

    if role == EnumUserRoles.GUEST:
        return common_rights | { EnumCommands.REGISTER: "Зарегистрироваться" }
    elif role == EnumUserRoles.STUDENT:
        return authed_user_rights | student_rights
    elif role == EnumUserRoles.MENTOR:
        return authed_user_rights | mentor_rights
    elif role == EnumUserRoles.MODER:
        return authed_user_rights | moder_rights
    elif role == EnumUserRoles.ADMIN:
        return authed_user_rights | admin_rights


def get_events_inline_kb(event_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text="Зарегистрироваться",
            callback_data=f"register_to_event:{event_id}",
        ),
    )

    return builder


def get_answer_question_inline_kb(question_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text="Ответить",
            callback_data=f"answer_a_question:{question_id}",
        ),
    )

    return builder
