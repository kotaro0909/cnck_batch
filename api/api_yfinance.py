import datetime
from logging import getLogger

import yfinance
from pandas import DataFrame

from common.db_maria_tx import DbMariaTx

# 記載サンプル
# api_yfinance.getAllToCsv()

# print(data.dtypes)
# データ構造
# 1: pen            float64
# 2: High            float64
# 3: Low             float64
# 4: Close           float64
# 5: Volume          int64
# 6: Dividends       float64
# 7: Stock Splits    float64

SYMBOL_ETH = "ETH-JPY"  # 仮想通貨の銘柄
SYMBOL_BTC = "BTC-JPY"  # 仮想通貨の銘柄
SYMBOLS = [SYMBOL_ETH, SYMBOL_BTC]

logger = getLogger(__name__)


def get_history(symbol: str):
    logger.debug(f"get history [symbol: {symbol}] - start")

    Ticker = yfinance.Ticker(symbol)
    data = Ticker.history(period="max")

    logger.debug(f"symbol: {symbol} \r\ndata: \r\n{data} \r\nget history [symbol: {symbol}] - end")
    return data


def toCsv(symbol: str, data: DataFrame):
    fileName = f"yfinace_{symbol}.txt"
    data = data.to_csv(fileName, header=True, index=True, encoding="utf8")
    print(data)


def getAllToCsv():
    for symbol in SYMBOLS:
        data = get_history(symbol)
        toCsv(symbol, data)


def insertAll():
    logger.debug("insertAll - Start")
    db = DbMariaTx()
    db.connect()

    sql_str = "insert into history (" \
              "symbol, hist_date, open_val, high_val, low_val, close_val, volume" \
              ")" \
              "values (?, ?, ?, ?, ?, ?, ?);"

    db.execute("delete from history")

    for symbol in SYMBOLS:
        is_first = True
        data = get_history(symbol)

        logger.debug(f"Insert history to db [{symbol}] - Start")
        for row in data.itertuples():
            if is_first:
                is_first = False
            else:
                dt = datetime.datetime(row[0].year, row[0].month, row[0].day, row[0].hour, row[0].minute, row[0].second)
                params = (symbol, dt, row[1], row[2], row[3], row[4], row[5])
                sql_sel = "select count(*) from history where symbol = ? and hist_date = ?;"
                db.execute(sql_str, params)
        logger.debug(f"Insert history to db [{symbol}] - End")

    db.commit()
    db.close()
    logger.debug("insertAll - End")


def test_retrieve_data():
    logger.info("1-1 BTCのデータ取得 - start")
    btc_data = get_history(SYMBOL_BTC)
    logger.info(f"BTC Data: {len(btc_data)} 件")
    logger.info("1-1 BTCのデータ取得 - end")

    logger.info("1-2 ETHのデータ取得 - start")
    eth_data = get_history(SYMBOL_ETH)
    logger.info(f"BTC Data: {len(eth_data)} 件")
    logger.info("1-2 ETHのデータ取得 - end")


def test_insert_db_all():
    insertAll()
