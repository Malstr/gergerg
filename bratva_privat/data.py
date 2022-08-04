from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    category_choice = State()
    text = State()
    photo_request = State()
    photo = State()
    send_request = State()
    block_id = State()
    access_id = State()
    access_days = State()
    add_admin_id = State()
    delete_admin_id = State()


class Menu(StatesGroup):
    period_choice = State()
    token_choice = State()
    network_choice = State()
    pay = State()

    choice = State()
    category_choice = State()


categories_url = {
    "temki": -1001757035252,
    "wax": -1001525249182,
    "arbitrage": -1001699359263,
    "premint": -1001751768463,
    "nft": -1001257016036,
    "lowbank": -1001718801388,
    "articles": -1001530655305,
    "softs": -1001650150936,
    "nodes": -1001770353417,
    "news": -1001604990299,
    "different": -1001558460186
}

wallets = {
    "USDT": {"SOL": "Erp7VFphoz5457gk4x7ZnoZSyvFwLxenieVBoz3UN5h6",
             "BEP20": "0x49255e5d93f896639266b6bf4bdb52b6ab390537",
             "TRC20": "TRAgwQFF1hLW15QoEbmyyoRmPFrSbv7RmF"},

    "USDC": {"SOL": "Erp7VFphoz5457gk4x7ZnoZSyvFwLxenieVBoz3UN5h6"},

    "BUSD": {"BEP20": "0x49255e5d93f896639266b6bf4bdb52b6ab390537"}
}