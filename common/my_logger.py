from logging import Formatter, StreamHandler, getLogger, DEBUG, INFO
from logging.handlers import TimedRotatingFileHandler


def consoleHandler():
    pass


def root_logger(output_path_log: str, level: int):
    # root loggerを取得
    logger = getLogger()

    # 既にハンドラーが設定されていれば何もしない
    if logger.hasHandlers():
        return logger

    # formatterを作成
    formatter = Formatter('%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s')
    # filename
    filename = f'{output_path_log}\\test.log'
    print(filename)

    # 例）コンソールに出力するハンドラ
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level)

    # 例）時間でローテーションするファイルを出力するハンドラ
    file_handler = TimedRotatingFileHandler(
        filename, when='D', interval=1, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    file_handler.setLevel(level)

    return logger
