from aiogram import types

class EnumUserRole:
    MODER = "moder"
    ADMIN = "admin"
    REGULAR = "regular"

type TRedis = dict[int, dict["role": EnumUserRole]]

redis: TRedis = {
    5478105927: {"role": EnumUserRole.MODER}
}

kb = [
        [
            types.KeyboardButton(text="Быстро"),
            types.KeyboardButton(text="В своем порядке")
        ],
    ]