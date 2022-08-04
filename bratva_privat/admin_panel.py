import sqlite3
from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext

from bot import dp, bot
from config import admin_id

from aiogram.types import Message, CallbackQuery, ContentTypes, ReplyKeyboardRemove

from data import Admin, categories_url, Menu
from keyboards import request_keyboard, categories2_choice_keyboard, menu_keyboard


@dp.message_handler(state="*", chat_id=admin_id, commands=["add_admin"])
async def get_admin_id(message: Message):
    await message.answer("Введи id пользователя")
    await Admin.add_admin_id.set()


@dp.message_handler(state=Admin.add_admin_id)
async def add_admin(message: Message, state: FSMContext):
    user_id = message.text

    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO admins VALUES(?)', (user_id,))
        db.commit()
        await message.answer("Админ успешно добавлен!")
    except:
        await message.answer("Не удалось добавить админа!")
    db.close()
    await state.finish()


@dp.message_handler(state="*", chat_id=admin_id, commands=["delete_admin"])
async def get_admin_id(message: Message):
    await message.answer("Введи id пользователя")
    await Admin.delete_admin_id.set()


@dp.message_handler(state=Admin.delete_admin_id)
async def delete_admin(message: Message, state: FSMContext):
    user_id = message.text

    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    try:
        cursor.execute('DELETE FROM admins WHERE id = ?', (user_id,))
        db.commit()
        await message.answer("Админ успешно удалён!")
    except:
        await message.answer("Не удалось удалить админа!")
    db.close()
    await state.finish()


@dp.message_handler(state="*", chat_id=admin_id, commands=["access"])
async def give_access(message: Message):
    await message.answer("Отправь id пользователя")
    await Admin.access_id.set()


@dp.message_handler(state=Admin.access_id)
async def give_access(message: Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    await message.answer("Введи кол-во дней")
    await Admin.access_days.set()


@dp.message_handler(state=Admin.access_days)
async def give_access(message: Message, state: FSMContext):
    days = message.text
    try:
        days = int(days)
        end_date = datetime.now() + timedelta(days=days)
        data = await state.get_data()
        user_id = data.get("user_id")
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO users VALUES(?,?)", (user_id, end_date))
        db.commit()
        db.close()
        await message.answer(f"Пользователь добавлен на {days} дней")
        await state.finish()
    except:
        await message.answer("Неправильное кол-во дней")


@dp.message_handler(state="*", chat_id=admin_id, commands=["block"])
async def get_block_id(message: Message):
    await message.answer("Введи id пользователя")
    await Admin.block_id.set()


@dp.message_handler(state=Admin.block_id)
async def block_id(message: Message, state: FSMContext):
    user_id = message.text

    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        await message.answer("Неверный id")
    else:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        cursor.execute("DELETE FROM categories WHERE user_id = ?", (user_id,))
        db.commit()
    db.close()
    await message.answer("Пользователь успешно заблокирован!")
    await state.finish()


@dp.message_handler(state="*", chat_id=admin_id, commands=["open"])
async def open_access(message: Message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("UPDATE access SET access = ?", (1,))
    db.commit()
    db.close()
    await message.answer("Набор открыт!")


@dp.message_handler(state="*", chat_id=admin_id, commands=["close"])
async def close_access(message: Message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("UPDATE access SET access = ?", (0,))
    db.commit()
    db.close()
    await message.answer("Набор закрыт!")


@dp.message_handler(state="*", commands=["send"])
async def send(message: Message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM admins WHERE id = ?", (message.from_user.id,))
    if cursor.fetchone() is not None:
        await message.answer("Выбери категорию для рассылки", reply_markup=categories2_choice_keyboard)
        await Admin.category_choice.set()


@dp.callback_query_handler(state=Admin.category_choice, text_startswith="2choice")
async def get_category(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except:
        pass

    category = call.data[8:]
    await state.update_data(category=category)

    await call.message.answer("Отправь текст для рассылки")
    await Admin.text.set()


@dp.message_handler(state=Admin.text)
async def get_text(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)

    await message.answer("Добавить фото?", reply_markup=request_keyboard)
    await Admin.photo_request.set()


@dp.message_handler(state=Admin.photo_request)
async def get_request(message: Message, state: FSMContext):
    if message.text == "Да":
        await message.answer("Отправь фото для рассылки")
        await Admin.photo.set()
    elif message.text == "Нет":
        data = await state.get_data()
        text = data.get("text")
        await message.answer(text)
        await message.answer("Отправить рассылку?", reply_markup=request_keyboard)
        await Admin.send_request.set()


@dp.message_handler(state=Admin.photo, content_types=ContentTypes.PHOTO)
async def get_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)

    data = await state.get_data()
    text = data.get("text")
    await message.answer_photo(photo=photo, caption=text)
    await message.answer("Отправить рассылку?", reply_markup=request_keyboard)
    await Admin.send_request.set()


@dp.message_handler(state=Admin.send_request, text="Да")
async def send_message(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    text = data.get("text")
    photo = data.get("photo")

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("SELECT user_id FROM categories WHERE category = ?", (category,))
    users = cursor.fetchall()
    db.close()

    await message.answer("Отправка рассылки...", reply_markup=ReplyKeyboardRemove())
    for user in users:
        try:
            if photo is not None:
                await bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            else:
                await bot.send_message(chat_id=user[0], text=text)
        except Exception as e:
            print(e)

    if photo is not None:
        await bot.send_photo(chat_id=categories_url[category], photo=photo, caption=text)
    else:
        await bot.send_message(chat_id=categories_url[category], text=text)

    await message.answer("Рассылка успешно выполнена ✅", reply_markup=menu_keyboard)
    await state.finish()
    await Menu.choice.set()


@dp.message_handler(state=Admin.send_request, text="Нет")
async def cancel_send_message(message: Message, state: FSMContext):
    await message.answer("Ок", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state="*", chat_id=admin_id, commands=["stats"])
async def get_stats(message: Message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    categories = categories_url.keys()
    stats = {}
    for category in categories:
        cursor.execute("SELECT * FROM categories WHERE category = ?", (category,))
        count = len(cursor.fetchall())
        stats[category] = count
    db.close()
    await message.answer(f"Статистика пользователей:\n\n"
                         f"📝ТЕМКИ: {stats['temki']}\n"
                         f"📙WAX: {stats['wax']}\n"
                         f"🎯ARBITRAGE: {stats['arbitrage']}\n"
                         f"🎲PREMINT: {stats['premint']}\n"
                         f"🎰NFT: {stats['nft']}\n"
                         f"🍭LOWBANK: {stats['lowbank']}\n"
                         f"📜БИБЛИОТЕКА: {stats['articles']}\n"
                         f"⚙️СОФТЫ: {stats['softs']}\n"
                         f"🛠НОДЫ: {stats['nodes']}\n"
                         f"📫НОВОСТИ: {stats['news']}\n"
                         f"🔧РАЗНОЕ: {stats['different']}\n")
