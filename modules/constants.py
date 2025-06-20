class EnumCommands:
    START = "start"
    CANCEL = "cancel"
    INFO = "info"
    CREATE_EVENT = "create_event"
    EVENTS = "events"
    ACTIVE_EVENTS = "active_events"
    ASK = "ask"
    VOTE_PROJECT = "vote_project"
    REGISTER = "register"
    LOGOUT = "logout"
    PROFILE = "profile"
    ADD_MENTOR = "add_mentor"
    ADD_MENTOR_TO_PROJECT = "add_projects_mentor"
    GET_MENTORS = "mentors"


class EnumUserRoles:
    GUEST = "Гость"
    MENTOR = "Преподаватель"
    STUDENT = "Ученик"
    MODER = "Организатор"
    ADMIN = "Админ"


class EnumStorageTokens:
    COMMAND_IN_ACTION = "command_in_action"
    USER_ID = "user_id"
