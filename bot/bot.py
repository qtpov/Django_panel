from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import asyncpg
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def create_db_connection():
    return await asyncpg.connect(DATABASE_URL)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.reply("Привет! Я ваш бот.")

@dp.message_handler(commands=['check_subscription'])
async def check_subscription(message: types.Message):
    conn = await create_db_connection()
    user_id = message.from_user.id
    result = await conn.fetchrow('SELECT * FROM subscriptions WHERE user_id = $1', user_id)
    if result:
        await message.reply("Вы подписаны.")
    else:
        await message.reply("Вы не подписаны.")
    await conn.close()

if __name__ == '__main__':
    logger.add("bot.log", rotation="10 MB")
    executor.start_polling(dp, skip_updates=True)