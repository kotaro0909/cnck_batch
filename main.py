import logging
import os
from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI
from api import api_coincheck
from common import my_logger
from routers.router_base import router as router_base
from routers.router_ticker import router as router_ticker

TICKER_STATE_STOP = "stopped"
TICKER_STATE_RUN = "running"
th1 = ThreadPoolExecutor()
log_path = f'{os.getcwd()}\\logs'
logger = my_logger.root_logger(log_path, level=logging.DEBUG)

app = FastAPI()
app.include_router(router_base)
app.include_router(router_ticker)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True, log_level="info")
    api_coincheck.update_State(TICKER_STATE_STOP)
