from aiogram import Dispatcher, Bot
import user_handlers
import other_handlers
from config import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user_handlers.router)
dp.include_router(other_handlers.router)

if __name__ == '__main__':
    dp.run_polling(bot)