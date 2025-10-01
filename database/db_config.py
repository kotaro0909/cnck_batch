"""
データベース設定
"""
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session

# データベース接続情報
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "cryptocurrency"

# 接続URL作成
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    echo=False,  # SQL ログ出力 (開発時は True にすると便利)
    pool_pre_ping=True,  # 接続の健全性チェック
    pool_recycle=3600,  # 1時間でコネクションを再生成
)

# セッションファクトリー
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()


def get_db() -> Generator[Session, Any, None]:
    """
    データベースセッションを取得するジェネレーター
    FastAPI の依存性注入で使用
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()