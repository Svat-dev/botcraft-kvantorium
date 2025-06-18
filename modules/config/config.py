from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from aiogram import Bot

class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()

bot = Bot(token=config.bot_token.get_secret_value())