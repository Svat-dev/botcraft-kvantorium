import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token="7825350159:AAE7xkTmZSgRbxRG18fsdDQ3QO7SHRIDn5o")

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("telljoke"))
async def tell_joke(message: types.Message):
    joke = "Колобок повесился"
    message.answer(joke)

@dp.message(Command("getweather"))
async def get_weather(message: types.Message):
    weather = "Сейчас солнечно! Осадков не ожидется"
    message.answer(weather)

@dp.message(Command("getdate"))
async def get_date(message: types.Message):
    date = f"Сейчас: {datetime.now().strftime('%H:%M:%S')}"
    message.answer(date)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())