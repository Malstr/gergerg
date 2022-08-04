import sqlite3

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import bot, dp
from data import Menu, categories_url
from keyboards import period_keyboard

scheduler = AsyncIOScheduler()


async def end_period(user_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM categories WHERE user_id = ?", (user_id,))
    db.commit()
    db.close()
    channels = categories_url.values()
    for channel in channels:
        try:
            await bot.kick_chat_member(chat_id=channel, user_id=user_id)
        except Exception as e:
            print(e)
    await bot.send_message(chat_id=user_id, text="Твоя подписка, к сожалению, закончилась\n\n"
                                                 "Для возобновления доступа - оплати подписку",
                           reply_markup=period_keyboard)
    await dp.storage.set_state(chat=user_id, state=Menu.period_choice)


def set_end_period():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchall()
    db.close()

    for user in user_data:
        user_id = user[0]
        end_date = user[1]
        scheduler.add_job(end_period, "date", run_date=end_date,
                          args=(user_id,))

