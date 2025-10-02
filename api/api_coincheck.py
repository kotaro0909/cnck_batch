import datetime
from logging import getLogger
from time import sleep

from database import db_config
from database.db_config import get_db
import requests
import json
from sqlalchemy.orm import Session
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


def update_state(db: Session, state: str):
    logger.debug(f"update - start")
    TickerStateRepository.update_state(db, state)
    logger.debug(f"update - finished")

def get_state(db: Session) -> str:
    logger.debug(f"get state - start")
    state = TickerStateRepository.get_state(db)
    logger.debug(f"get state - end")
    return state


def get_ticker(db: Session, symbol: str):
    url = BASE_URL + "/api/ticker"
    rtn = requests.get(url, params={"pair": symbol})
    logger.debug(f"called api.")
    json_dat = json.loads(rtn.text)
    json_dat["tick_datetime"] = datetime.datetime.fromtimestamp(json_dat["timestamp"])
    json_dat['symbol'] = symbol
    TickHistoryRepository.insert(db, json_dat)
    logger.debug(f"add tick data.")


def ticker_run(db: Session) -> bool:
    message = get_state(db)
    logger.debug(f"current state is {message}.")

    if message == TICKER_STATE_STOP:
        flag = False
    else:
        flag = True
        for symbol in SYMBOLS:
            logger.debug(f"get_tick(symbol: {symbol}) - start")
            get_ticker(db, symbol)
            logger.debug(f"get_tick(symbol: {symbol}) - end")

    return flag


def ticker_run_main():
    flag = True
    while flag:
        logger.info("ticker tick - start")
        db = next(get_db())
        flag = ticker_run(db)
        db.close()
        logger.info("ticker tick - end")
        sleep(15)