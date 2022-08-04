import sqlite3
from datetime import datetime, timedelta, date

from aiogram.dispatcher import FSMContext
from binance import Client

from data import Menu, wallets
from keyboards import categories_choice_keyboard, menu_keyboard, categories_archive_keyboard, period_keyboard, \
    tokens_keyboard, back_keyboard
from bot import dp

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest

from scheduler import scheduler, end_period


@dp.chat_join_request_handler()
async def approve_request(request: ChatJoinRequest):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (request.from_user.id,))
    if cursor.fetchone() is not None:
        await dp.bot.approve_chat_join_request(chat_id=request.chat.id, user_id=request.from_user.id)
    db.close()


@dp.message_handler(state="*", commands="start")
async def start_message(message: Message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
    if cursor.fetchone() is None:
        cursor.execute("SELECT access FROM access")
        access = cursor.fetchone()[0]
        if access == 1:
            await message.answer("Для доступа к приватным каналам нужно оплатить подписку\n\n"
                                 "Выбери тариф", reply_markup=period_keyboard)
        else:
            await message.answer("На данный момент набор закрыт!")
    else:
        cursor.execute("SELECT * FROM categories WHERE user_id = ?", (message.from_user.id,))
        if cursor.fetchone() is None:
            await message.answer("Выбери категории", reply_markup=categories_choice_keyboard)
        else:
            await message.answer("🖐🏻Привет и добро пожаловать в Братву Мальстрёма!\n\n"
                                 "Подпишись на интересующие тебя темы, откинься на стуле и наслаждайся нашей работой!"
                                 "\n\nЧто-то пропустил? Просто загляни в Архив📚!", reply_markup=menu_keyboard)
            await Menu.choice.set()
    db.close()


@dp.callback_query_handler(state="*", text_startswith="period")
async def get_period(call: CallbackQuery, state: FSMContext):
    months = int(call.data[7])
    await state.update_data(months=months)

    await call.message.edit_text(text="Выбери токен", reply_markup=tokens_keyboard)
    await Menu.token_choice.set()


@dp.callback_query_handler(state=Menu.token_choice, text="token_back")
async def token_back(call: CallbackQuery):
    await call.message.edit_text("Выбери тариф", reply_markup=period_keyboard)
    await Menu.period_choice.set()


@dp.callback_query_handler(state=Menu.token_choice, text_startswith="token")
async def get_token(call: CallbackQuery, state: FSMContext):
    token = call.data[6:]
    await state.update_data(token=token)

    networks_keyboard = InlineKeyboardMarkup()
    networks = wallets[token].keys()
    for network in networks:
        button = InlineKeyboardButton(text=network, callback_data=f"network_{network}")
        networks_keyboard.add(button)
    button = InlineKeyboardButton(text="Назад", callback_data="network_back")
    networks_keyboard.add(button)
    await call.message.edit_text(text="Выбери сеть", reply_markup=networks_keyboard)
    await Menu.network_choice.set()


@dp.callback_query_handler(state=Menu.network_choice, text="network_back")
async def network_back(call: CallbackQuery):
    await call.message.edit_text(text="Выбери токен", reply_markup=tokens_keyboard)
    await Menu.token_choice.set()


@dp.callback_query_handler(state=Menu.network_choice, text_startswith="network")
async def get_network(call: CallbackQuery, state: FSMContext):
    network = call.data[8:]
    await state.update_data(network=network)

    data = await state.get_data()
    months = data.get("months")
    token = data.get("token")
    network = data.get("network")

    price = 49 if months == 1 else 89
    await state.update_data(price=price)
    wallet = wallets[token][network]

    await call.message.edit_text(text=f"<b>{token} ({network})</b>\n\n"
                                      f"Сумма: <b>{price} {token}</b>\n"
                                      f"Кошелёк: <code>{wallet}</code>\n\n"
                                      f"После оплаты - отправь хэш транзакции в чат", reply_markup=back_keyboard)
    await Menu.pay.set()


@dp.callback_query_handler(state=Menu.pay, text="back")
async def pay_back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    token = data.get("token")

    networks_keyboard = InlineKeyboardMarkup()
    networks = wallets[token].keys()
    for network in networks:
        button = InlineKeyboardButton(text=network, callback_data=f"network_{network}")
        networks_keyboard.add(button)
    button = InlineKeyboardButton(text="Назад", callback_data="network_back")
    networks_keyboard.add(button)
    await call.message.edit_text(text="Выбери сеть", reply_markup=networks_keyboard)
    await Menu.network_choice.set()


@dp.message_handler(state=Menu.pay)
async def get_hash(message: Message, state: FSMContext):
    data = await state.get_data()
    months = data.get("months")
    token = data.get("token")
    price = data.get("price")
    payment_hash = message.text

    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM hashs WHERE hash = ?", (payment_hash,))
    if cursor.fetchone() is None:
        api_key = "c7pq31tIIxxb8qHtaxMPcncoU96hRheITcj3kYR8uwLrCp647wgQzBBGaYkv40Wh"
        api_secret = "5Kb2JgATMyYs74Tu1iGpILRAr0ZCYPEmfMTNyGW0fLIqXcWzyT55M5Xgt1uCRXhq"
        client = Client(api_key, api_secret)

        transactions = client.get_deposit_history(coin=token)

        for transaction in transactions:
            if transaction["txId"] == payment_hash and float(transaction["amount"]) >= price - 1:
                cursor.execute("SELECT end_date FROM users WHERE id = ?", (message.from_user.id,))
                end_date = cursor.fetchone()
                if end_date is None:
                    end_date = datetime.now() + timedelta(days=months*30)
                    cursor.execute("INSERT INTO users VALUES(?,?)", (message.from_user.id, end_date))
                    db.commit()
                else:
                    end_date = datetime.fromisoformat(end_date[0]) + timedelta(days=months*30)
                    cursor.execute("UPDATE users SET end_date = ? WHERE id = ?", (end_date, message.from_user.id))
                    db.commit()

                cursor.execute("INSERT INTO hashs VALUES(?)", (payment_hash,))
                db.commit()
                scheduler.add_job(end_period, "date", run_date=end_date,
                                  args=(message.from_user.id,))
                await message.answer("Оплата успешно прошла ✅")
                cursor.execute("SELECT * FROM categories WHERE user_id = ?", (message.from_user.id,))
                if cursor.fetchone() is None:
                    await message.answer("Выбери категории", reply_markup=categories_choice_keyboard)
                    await Menu.category_choice.set()
                else:
                    await message.answer("Главное Меню", reply_markup=menu_keyboard)
                    await Menu.choice.set()
                break
        else:
            await message.answer("Хэш транзакции не найден! \n "
                                 "Попробуй еще раз через минуту, скорее всего транзакция еще не дошла 👀")
    else:
        await message.answer("Хэш уже использован! 🤔")

    db.close()


@dp.callback_query_handler(state="*", text_startswith="choice")
async def category_choice(call: CallbackQuery, state: FSMContext):
    category = call.data
    data = await state.get_data()
    categories_edit_keyboard = data.get("categories_edit_keyboard")

    if categories_edit_keyboard is None:
        buttons = categories_choice_keyboard["inline_keyboard"]
    else:
        buttons = categories_edit_keyboard["inline_keyboard"]

    categories_edit_keyboard = InlineKeyboardMarkup()
    for button in buttons:
        text = button[0]["text"]
        callback_data = button[0]["callback_data"]
        if callback_data == category:
            if " ✅" in text:
                text = text[:-2]
            else:
                text += " ✅"
        res_button = InlineKeyboardButton(text=text, callback_data=callback_data)
        categories_edit_keyboard.add(res_button)

    await state.update_data(categories_edit_keyboard=categories_edit_keyboard)
    await call.message.edit_reply_markup(reply_markup=categories_edit_keyboard)


@dp.callback_query_handler(state="*", text_startswith="make_choice")
async def category_choice(call: CallbackQuery, state: FSMContext):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories WHERE user_id = ?", (call.from_user.id,))
    if cursor.fetchone() is not None:
        cursor.execute("DELETE FROM categories WHERE user_id = ?", (call.from_user.id,))
        db.commit()

    data = await state.get_data()
    categories_edit_keyboard = data.get("categories_edit_keyboard")
    if categories_edit_keyboard is None:
        await call.answer("Ты не выбрал ни одной категории 🙁", show_alert=True)
    else:
        buttons = categories_edit_keyboard["inline_keyboard"]
        result_categories = []

        for button in buttons:
            if " ✅" in button[0]["text"]:
                result_categories.append(button[0]["callback_data"][7:])

        if len(result_categories) == 0:
            await call.answer("Ты не выбрал ни одной категории 🙁", show_alert=True)
        else:
            for category in result_categories:
                cursor.execute("INSERT INTO categories VALUES(?,?)", (call.from_user.id, category))
                db.commit()

            try:
                await call.message.delete()
            except:
                pass

            await state.finish()
            await call.message.answer("Вы успешно выбрали категории!", reply_markup=menu_keyboard)
            await Menu.choice.set()
    db.close()


@dp.message_handler(state=Menu.choice, text="Редактировать категории")
async def edit_categories(message: Message, state: FSMContext):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT category FROM categories WHERE user_id = ?", (message.from_user.id,))
    categories = [category[0] for category in cursor.fetchall()]
    db.close()

    buttons = categories_choice_keyboard["inline_keyboard"]
    categories_edit_keyboard = InlineKeyboardMarkup()
    for button in buttons:
        text = button[0]["text"]
        callback_data = button[0]["callback_data"]
        if callback_data[7:] in categories:
            text += " ✅"
        res_button = InlineKeyboardButton(text=text, callback_data=callback_data)
        categories_edit_keyboard.add(res_button)

    await state.update_data(categories_edit_keyboard=categories_edit_keyboard)
    await message.answer("Выбери категории", reply_markup=categories_edit_keyboard)


@dp.message_handler(state=Menu.choice, text="Архив 📚")
async def archive(message: Message):
    await message.answer("Архив какой темы тебя интересует?", reply_markup=categories_archive_keyboard)


@dp.message_handler(state=Menu.choice, text="Личный кабинет🐳")
async def my_subscription(message: Message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT end_date FROM users WHERE id = ?", (message.from_user.id,))
    end_date = datetime.fromisoformat(cursor.fetchone()[0]).strftime("%d.%m.%y")
    await message.answer(f"⚙️Дата окончания подписки: <b>{end_date}</b>\n\n"
                         f"Вы можете продлить подписку прямо сейчас! \n\n 🔁Доступные тарифы:", reply_markup=period_keyboard)








































