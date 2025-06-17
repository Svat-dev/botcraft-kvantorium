from aiogram import types

class EnumUserRole:
    MODER = "moder"
    ADMIN = "admin"
    REGULAR = "regular"

redis = [
    {0: {"role": "none"}},
    {5478105927: {"role": EnumUserRole.MODER, "passwrod": "12345678"}}
]

kb = [
        [
            types.KeyboardButton(text="Быстро"),
            types.KeyboardButton(text="В своем порядке")
        ],
    ]