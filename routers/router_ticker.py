from logging import getLogger
from time import sleep
from fastapi import APIRouter, Depends

import routers.router_base
from api import api_coincheck
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from common.db_config import get_db

from common.db_repositories import TickerStateRepository, TickHistoryRepository

TICKER_STATE_STOP = routers.router_base.TICKER_STATE_STOP
TICKER_STATE_RUN = routers.router_base.TICKER_STATE_RUN
th1 = ThreadPoolExecutor()
router = APIRouter()

logger = getLogger(__name__)



@router.get("/ticker/status")
async def ticker_status(db: Session = Depends(get_db)):
    """Ticker 状態を取得"""
    state = TickerStateRepository.get_state(db)
    logger.info(f"ticker status: {state}")
    return {"status": state}

@router.post("/ticker/start")
async def ticker_start(db: Session = Depends(get_db)):
    """Ticker を開始"""
    TickerStateRepository.update_state(db, "running")
    logger.info("ticker start running")
    return {"message": "Ticker started"}

@router.post("/ticker/stop")
async def ticker_stop(db: Session = Depends(get_db)):
    """Ticker を停止"""
    TickerStateRepository.update_state(db, "stopped")
    logger.info("ticker stopped")
    return {"message": "Ticker stopped"}

@router.get("/ticker/history/{symbol}")
async def get_history(symbol: str, limit: int = 100, db: Session = Depends(get_db)):
    """ティック履歴を取得"""
    history = TickHistoryRepository.get_by_symbol(db, symbol, limit=limit)
    return {"symbol": symbol, "count": len(history), "data": history}


# def ticker_run_main():
#     while True:
#         message = api_coincheck.get_state()
#         if message == TICKER_STATE_STOP:
#             break
#         api_coincheck.all_tick()
#         sleep(600)


###
# ここより下は変換済み
###

# @router.get("/ticker/status")
# def ticker_status():
#     message = api_coincheck.get_state()
#     logger.info(f"ticker status: {message}")
#     return {"ticker": f"{message}"}
#
#
# @router.get("/ticker/stop")
# def ticker_stop():
#     api_coincheck.update_State(TICKER_STATE_STOP)
#     th1.shutdown(wait=True)
#     logger.info("ticker stopped")
#     return {"ticker": TICKER_STATE_STOP}
#
#
# @router.get("/ticker/run")
# def ticker_run():
#     api_coincheck.update_State(TICKER_STATE_RUN)
#     th1.submit(ticker_run_main)
#     logger.info("ticker start running")
#     return {"ticker": TICKER_STATE_RUN}
#
#

