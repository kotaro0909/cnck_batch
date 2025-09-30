"""
データベースモデル定義
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from datetime import datetime
from common.db_config import Base


class TickerState(Base):
    """Ticker 状態管理テーブル"""
    __tablename__ = "ticker_state"

    id = Column(Integer, primary_key=True)
    state = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<TickerState(id={self.id}, state='{self.state}')>"


class TickHistory(Base):
    """ティック履歴テーブル"""
    __tablename__ = "tick_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tick_datetime = Column(DateTime, nullable=False, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    last = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    # 複合インデックス
    __table_args__ = (
        Index('idx_symbol_datetime', 'symbol', 'tick_datetime'),
    )

    def __repr__(self):
        return f"<TickHistory(symbol='{self.symbol}', datetime={self.tick_datetime}, last={self.last})>"