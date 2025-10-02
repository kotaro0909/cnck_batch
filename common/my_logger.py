import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG, INFO
from logging.handlers import TimedRotatingFileHandler


def consoleHandler():
    pass


def root_logger(output_path_log: str):
    # root loggerを取得
    logger = getLogger()
    # Traceログの代わりにDEBUGログを出力するため、ここではDEBUGを設定
    #     root loggerのログレベル以下はログ出力されなくなってしまうため一番低いレベルを設定
    #     Traceログ用と通常ログ用の２つのFileHandlerを用意して、2つのファイルにログ内容を出しわける
    logger.setLevel(DEBUG)

    # 既にハンドラーが設定されていれば何もしない
    if logger.hasHandlers():
        return logger

    # formatterを作成
    formatter = Formatter('%(asctime)s [%(levelname)s]: %(name)s:%(lineno)s %(funcName)s %(message)s')

    # 例）コンソールに出力するハンドラ
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    console_handler.setLevel(logging.DEBUG)

    #ログファイル名の規定部分の名称
    filename_base = "application"

    # 例）時間でローテーションするファイルを出力するハンドラ
    filename1 = f'{output_path_log}\\{filename_base}.log'
    file_handler1 = TimedRotatingFileHandler(
        filename1, when='D', interval=1, backupCount=10, encoding='utf-8'
    )
    file_handler1.setFormatter(formatter)
    logger.addHandler(file_handler1)
    file_handler1.setLevel(logging.INFO)

    # 例）時間でローテーションするファイルを出力するハンドラ デバッグログ
    filename2 = f'{output_path_log}\\{filename_base}-debug.log'
    file_handler2 = TimedRotatingFileHandler(
        filename2, when='D', interval=1, backupCount=5, encoding='utf-8'
    )
    file_handler2.setFormatter(formatter)
    logger.addHandler(file_handler2)
    file_handler2.setLevel(logging.DEBUG)
    # file_handler2.setLevel(level)
    return logger
