from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Редактировать категории")
        ],
        [
            KeyboardButton(text="Архив 📚"),
            KeyboardButton(text="Личный кабинет🐳")
        ]
    ],
    resize_keyboard=True
)


request_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да")
        ],
        [
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True
)


categories_choice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝ТЕМКИ", callback_data="choice_temki")
        ],
        [
            InlineKeyboardButton(text="📙WAX", callback_data="choice_wax")
        ],
        [
            InlineKeyboardButton(text="🎯ARBITRAGE", callback_data="choice_arbitrage")
        ],
        [
            InlineKeyboardButton(text="🎲PREMINT", callback_data="choice_premint")
        ],
        [
            InlineKeyboardButton(text="🎰NFT", callback_data="choice_nft")
        ],
        [
            InlineKeyboardButton(text="🍭LOWBANK", callback_data="choice_lowbank")
        ],
        [
            InlineKeyboardButton(text="📜БИБЛИОТЕКА", callback_data="choice_articles")
        ],
        [
            InlineKeyboardButton(text="⚙️СОФТЫ", callback_data="choice_softs")
        ],
        [
            InlineKeyboardButton(text="🛠НОДЫ", callback_data="choice_nodes")
        ],
        [
            InlineKeyboardButton(text="📫НОВОСТИ", callback_data="choice_news")
        ],
        [
            InlineKeyboardButton(text="🔧РАЗНОЕ", callback_data="choice_different")
        ],
        [
            InlineKeyboardButton(text="Выбрать", callback_data="make_choice"),
        ]
    ]
)


categories2_choice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝ТЕМКИ", callback_data="2choice_temki")
        ],
        [
            InlineKeyboardButton(text="📙WAX", callback_data="2choice_wax")
        ],
        [
            InlineKeyboardButton(text="🎯ARBITRAGE", callback_data="2choice_arbitrage")
        ],
        [
            InlineKeyboardButton(text="🎲PREMINT", callback_data="2choice_premint")
        ],
        [
            InlineKeyboardButton(text="🎰NFT", callback_data="2choice_nft")
        ],
        [
            InlineKeyboardButton(text="🍭LOWBANK", callback_data="2choice_lowbank")
        ],
        [
            InlineKeyboardButton(text="📜БИБЛИОТЕКА", callback_data="2choice_articles")
        ],
        [
            InlineKeyboardButton(text="⚙️СОФТЫ", callback_data="2choice_softs")
        ],
        [
            InlineKeyboardButton(text="🛠НОДЫ", callback_data="2choice_nodes")
        ],
        [
            InlineKeyboardButton(text="📫НОВОСТИ", callback_data="2choice_news")
        ],
        [
            InlineKeyboardButton(text="🔧РАЗНОЕ", callback_data="2choice_different")
        ]
    ]
)


categories_archive_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝ТЕМКИ", url="https://t.me/+3yzih52jQMVmMjE6")
        ],
        [
            InlineKeyboardButton(text="📙WAX", url="https://t.me/+M213Pbb8kgMzOGY6")
        ],
        [
            InlineKeyboardButton(text="🎯ARBITRAGE", url="https://t.me/+U4Rl4tlSBD9kYzcy")
        ],
        [
            InlineKeyboardButton(text="🎲PREMINT", url="https://t.me/+LwPdQ1e026E1YTMy")
        ],
        [
            InlineKeyboardButton(text="🎰NFT", url="https://t.me/+fQEkNKqWkiowMTJi")
        ],
        [
            InlineKeyboardButton(text="🍭LOWBANK", url="https://t.me/+HPBqCS3MNzs5Mjky")
        ],
        [
            InlineKeyboardButton(text="📜БИБЛИОТЕКА", url="https://t.me/+zNaN4MTvrLgyNzIy")
        ],
        [
            InlineKeyboardButton(text="⚙️СОФТЫ", url="https://t.me/+7jV-5vag5Tg4ZjBi")
        ],
        [
            InlineKeyboardButton(text="🛠НОДЫ", url="https://t.me/+Jgx0XbmP0RdmNTMy")
        ],
        [
            InlineKeyboardButton(text="📫НОВОСТИ", url="https://t.me/+RAgioaSczoNmMjEy")
        ],
        [
            InlineKeyboardButton(text="🔧РАЗНОЕ", url="https://t.me/+DWNWuseLFBE4ZWRi")
        ]
    ]
)

period_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 месяц", callback_data="period_1")
        ],
        [
            InlineKeyboardButton(text="3 месяца (-10%)", callback_data="period_3")
        ]
    ]
)


tokens_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="USDT", callback_data="token_USDT")
        ],
        [
            InlineKeyboardButton(text="USDC", callback_data="token_USDC")
        ],
        [
            InlineKeyboardButton(text="BUSD", callback_data="token_BUSD")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="token_back")
        ]
    ]
)

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ]
)