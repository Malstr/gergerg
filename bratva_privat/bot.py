import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    from handlers import dp
    from admin_panel import dp
    from scheduler import scheduler, set_end_period

    scheduler.start()
    executor.start_polling(dp,  on_startup=set_end_period())
