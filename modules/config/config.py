from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=storage)
