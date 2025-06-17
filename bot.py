import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from datetime import datetime

from config import config
from data import kb, redis

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите скорость выполнения"
    )

    await message.answer("Как быстро вы хотите получить IPhone 16 Pro Max?", reply_markup=keyboard)

    is_user_in_system = redis.get(message.from_user.id)

    if not is_user_in_system:
        await message.answer("Вы не в системе")
        return False
    
    current_role = is_user_in_system.get("role")
    await message.answer(current_role)

@dp.message(Command("register"))
async def register(message: types.Message):
    is_auth = redis.sort(message.from_user.id or 0)
    print(is_auth)
    # if is_auth != "none":
    #     await message.reply("Вы уже в системе")
    #     return False
    
    await message.reply("Идет создание...")

    user_id = message.from_user.id
    redis.append(user_id)
    print(redis)

@dp.message(F.text.lower() == "быстро")
async def make_it_fast(message: types.Message):
    await message.reply("С вас дополнительно 10 руб.")

@dp.message(F.text.lower() == "в своем порядке")
async def make_it_slow(message: types.Message):
    await message.reply("Вы получите его ровно через год")

@dp.message(Command("telljoke"))
async def tell_joke(message: types.Message):
    joke = "Колобок повесился"
    await message.answer(joke)

@dp.message(Command("getweather"))
async def get_weather(message: types.Message):
    weather = "Сейчас солнечно! Осадков не ожидется"
    await message.answer(weather)

@dp.message(Command("getdate"))
async def get_date(message: types.Message):
    date = f"Сейчас: {datetime.now().strftime('%H:%M:%S')}"
    await message.answer(date)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())