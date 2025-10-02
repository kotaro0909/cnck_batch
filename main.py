import logging
import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from api import api_coincheck
from common import my_logger, uvicorn_log_config
from routers.router_base import router as router_base
from routers.router_ticker import router as router_ticker
from database.db_config import get_db

# 定期繰り返し実行のTicker実行用のスレッド
th1 = ThreadPoolExecutor()

#ログ共通設定
log_path = f'{os.getcwd()}\\logs'

# Root Loggerの設定
logger = my_logger.root_logger(log_path)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # 起動時の処理
    logger.info("Application starting up...")
    db = next(get_db())
    try:
        api_coincheck.update_state(db, api_coincheck.TICKER_STATE_STOP)
        logger.info("Initialization completed")
        yield  # アプリケーション実行中
    finally:
        # 終了時の処理
        logger.info("Application shutting down...")
        # クリーンアップ処理があればここに書く


app = FastAPI(lifespan=lifespan)
app.include_router(router_base)
app.include_router(router_ticker)

if __name__ == '__main__':
    logconf = uvicorn_log_config.get_log_config(log_path)
    uvicorn.run("main:app", port=8080, reload=True, log_config=logconf)
