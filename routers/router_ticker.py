from logging import getLogger
from time import sleep
from fastapi import APIRouter

import routers.router_base
from api import api_coincheck
from concurrent.futures import ThreadPoolExecutor

TICKER_STATE_STOP = routers.router_base.TICKER_STATE_STOP
TICKER_STATE_RUN = routers.router_base.TICKER_STATE_RUN
th1 = ThreadPoolExecutor()
router = APIRouter()

logger = getLogger(__name__)


@router.get("/ticker/status")
def ticker_status():
    message = api_coincheck.get_state()
    logger.info(f"ticker status: {message}")
    return {"ticker": f"{message}"}


@router.get("/ticker/stop")
def ticker_stop():
    api_coincheck.update_State(TICKER_STATE_STOP)
    th1.shutdown(wait=True)
    logger.info("ticker stopped")
    return {"ticker": TICKER_STATE_STOP}


@router.get("/ticker/run")
def ticker_run():
    api_coincheck.update_State(TICKER_STATE_RUN)
    th1.submit(ticker_run_main)
    logger.info("ticker start running")
    return {"ticker": TICKER_STATE_RUN}


def ticker_run_main():
    while True:
        message = api_coincheck.get_state()
        if message == TICKER_STATE_STOP:
            break
        api_coincheck.all_tick()
        sleep(600)
