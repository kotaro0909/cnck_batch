import sys
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter

TICKER_STATE_STOP = "stopped"
TICKER_STATE_RUN = "running"
th1 = ThreadPoolExecutor()

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello World"}

@router.post("/shutdown")
def shutdown():
    sys.exit()
