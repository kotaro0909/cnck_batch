import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger

from fastapi import APIRouter

th1 = ThreadPoolExecutor()
logger = getLogger(__name__)
router = APIRouter()


@router.get("/")
def root():
    logger.info("root")
    return {"message": "Hello World"}


@router.post("/shutdown")
def shutdown():
    """Uvicornサーバーを停止"""
    logger.info("Shutting down server...")

    # 現在のプロセスにSIGTERMシグナルを送信
    os.kill(os.getpid(), signal.SIGTERM)

    return {"message": "Server is shutting down"}
