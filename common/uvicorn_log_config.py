# uvicornログ設定
def get_log_config(log_dir: str) -> dict:
    custom_logging_config = {
        # ロギングの設定バージョン (固定で 1 を指定)
        "version": 1,

        # 既存のロガーを無効にしない (他のロガー設定を保持する)
        "disable_existing_loggers": False,

        # 【フォーマッターの設定】ログの出力フォーマットを定義
        "formatters": {
            # デフォルトのフォーマット (主に uvicorn.error で使用)
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s [%(levelname)s]: %(name)s:%(lineno)s %(funcName)s %(message)s",  # ログレベルとメッセージのみ出力
                "use_colors": False,  # ANSI カラー出力 (ターミナルによって自動調整)
            },
            # アクセスログのフォーマット (HTTP リクエスト情報を含む)
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(asctime)s [%(levelname)s]: %(name)s:%(lineno)s %(funcName)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # クライアントIP、リクエスト、ステータスコードを表示
                "use_colors": False,  # ANSI カラー出力 (ターミナルによって自動調整)
            },
        },

        # 【ハンドラーの設定】ログの出力先を定義
        "handlers": {
            # 標準ログの出力先
            "default": {
                "formatter": "default",  # 上記の "default" フォーマッターを使用
                "level": "INFO",
                "class": "logging.StreamHandler",  # 標準出力に送るストリームハンドラー
                "stream": "ext://sys.stderr",  # 出力先を標準エラー (stderr) に指定
            },
            # クリティカルログファイル出力
            "critical_file": {
                "formatter": "default",
                "level": "WARNING",
                "class": "logging.FileHandler",
                "filename": f"{log_dir}\\uvicorn_error.log"
            },
            # 通常ログファイル出力
            "normal_file": {
                "formatter": "default",
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": f"{log_dir}\\uvicorn.log"
            },
            # アクセスログファイル出力
            "access_file": {
                "formatter": "access",
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": f"{log_dir}\\access.log"
            },
        },

        # 【ロガーの設定】各ロガーが使用するハンドラーとログレベルを定義
        "loggers": {
            # メインの Uvicorn ロガー (デフォルトでは出力されない)
            "uvicorn": {
                "handlers": ["default","critical_file"],  # 標準ログのハンドラーを使用
                "level": "WARNING",  # ロガーではINFO レベル以上を出力
                "propagate": False,  # 他のロガーにログを伝播させない
            },
            # エラーログ (起動メッセージや例外ログを出力)
            "uvicorn.error": {
                "handlers": ["default","normal_file"],  # コンソールとエラーログファイルに出力
                "level": "INFO",  # ロガーではINFO レベル以上を出力
                "propagate": False,  # 他のロガーにログを伝播させない
            },
            # アクセスログロガー
            "uvicorn.access": {
                "handlers": ["default","access_file"],  # コンソールとアクセスログファイルに出力
                "level": "INFO",  # ロガーではINFO レベル以上を出力
                "propagate": False,  # 他のロガーにログを伝播させない
            },
        },
    }
    return custom_logging_config
