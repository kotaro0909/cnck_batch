import datetime
from logging import getLogger
from time import sleep

from database import db_config
from database.db_config import get_db
import requests
import json

import schedule

from common.db_maria_tx import DbMariaTx
from database.db_repositories import TickerStateRepository, TickHistoryRepository

SYMBOL_ETH = "eth_jpy"  # 仮想通貨の銘柄
SYMBOL_BTC = "btc_jpy"  # 仮想通貨の銘柄
SYMBOLS = [SYMBOL_ETH, SYMBOL_BTC]
TICKER_STATE_STOP = "stopped"
TICKER_STATE_RUN = "running"
BASE_URL = "https://coincheck.com"

logger = getLogger(__name__)

def update_state(state: str):
    TickerStateRepository.update_state(db_config.get_db(), state)

def get_state() -> str:
    state = TickerStateRepository.get_state(db_config.get_db())
    return state


def get_ticker(symbol: str):
    url = BASE_URL + "/api/ticker"
    rtn = requests.get(url, params={"pair": symbol})
    json_dat = json.loads(rtn.text)
    json_dat["tick_datetime"] = datetime.datetime.fromtimestamp(json_dat["timestamp"])
    json_dat['symbol'] = symbol
    print(json_dat)
    TickHistoryRepository.insert(db_config.get_db(), json_dat)


def ticker_run() -> bool:
    flag = True
    logger.info("ticker_run - start")
    message = get_state()
    logger.info(f"ticker_run - state: {message}")

    if message == TICKER_STATE_STOP:
        flag = False
    else:
        flag = True

    for symbol in SYMBOLS:
        logger.info(f"ticker_run - get_tick(symbol: {symbol}) - start")
        get_ticker(symbol)
        logger.info(f"ticker_run - get_tick(symbol: {symbol}) - end")

    logger.info("ticker_run - end")

    return flag


