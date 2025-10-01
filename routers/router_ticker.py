from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from time import sleep

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import api_coincheck
from database.db_config import get_db
from database.db_repositories import TickHistoryRepository

th1 = ThreadPoolExecutor()
router = APIRouter()

logger = getLogger(__name__)



@router.get("/ticker/status")
async def ticker_status(db: Session = Depends(get_db)):
    """Ticker 状態を取得"""
    state = api_coincheck.get_state()
    logger.info(f"ticker status: {state}")
    return {"status": state}

@router.post("/ticker/start")
async def ticker_start(db: Session = Depends(get_db)):
    """Ticker を開始"""
    api_coincheck.update_state(api_coincheck.TICKER_STATE_RUN)
    th1.submit(ticker_run_main)
    logger.info("ticker start running")
    return {"message": "Ticker started"}

@router.post("/ticker/stop")
async def ticker_stop(db: Session = Depends(get_db)):
    """Ticker を停止"""
    api_coincheck.update_state(api_coincheck.TICKER_STATE_STOP)
    logger.info("ticker stopped")
    return {"message": "Ticker stopped"}

@router.get("/ticker/history/{symbol}")
async def get_history(symbol: str, limit: int = 100, db: Session = Depends(get_db)):
    """ティック履歴を取得"""
    history = TickHistoryRepository.get_by_symbol(db, symbol, limit=limit)
    return {"symbol": symbol, "count": len(history), "data": history}


def ticker_run_main():
    flag = True
    while flag:
        logger.info("ticker tick - start")
        flag = api_coincheck.ticker_run()
        logger.info("ticker tick - end")
        sleep(15)