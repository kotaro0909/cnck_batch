"""
データベース操作用リポジトリ
"""
from datetime import datetime
from typing import Any, Generator
from typing import List, Optional

from sqlalchemy.orm import Session

from database.db_models import TickerState, TickHistory


class TickerStateRepository:
    """Ticker 状態管理リポジトリ"""

    @staticmethod
    def get_state(db: Session, ticker_id: int = 1) -> Optional[str]:
        """状態を取得"""
        state = db.query(TickerState).filter(TickerState.id == ticker_id).first()
        return state.state if state else None

    @staticmethod
    def update_state(db: Session, new_state: str, ticker_id: int = 1) -> bool:
        """状態を更新"""
        try:
            state = db.query(TickerState).filter(TickerState.id == ticker_id).first()
            if state:
                state.state = new_state
            else:
                state = TickerState(id=ticker_id, state=new_state)
                db.add(state)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e


class TickHistoryRepository:
    """ティック履歴リポジトリ"""

    @staticmethod
    def insert(db: Session, tick_data: dict) -> TickHistory:
        """ティックデータを挿入"""
        tick = TickHistory(
            tick_datetime=tick_data['tick_datetime'],
            symbol=tick_data['symbol'],
            last=tick_data['last'],
            bid=tick_data['bid'],
            ask=tick_data['ask'],
            high=tick_data['high'],
            low=tick_data['low'],
            volume=tick_data['volume']
        )
        db.add(tick)
        db.commit()
        # session.refresh(tick)
        return tick

    @staticmethod
    def get_by_symbol(
            db: Session,
            symbol: str,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            limit: int = 100
    ) -> List[TickHistory]:
        """シンボルでティック履歴を取得"""
        query = db.query(TickHistory).filter(TickHistory.symbol == symbol)

        if start_date:
            query = query.filter(TickHistory.tick_datetime >= start_date)
        if end_date:
            query = query.filter(TickHistory.tick_datetime <= end_date)

        return query.order_by(TickHistory.tick_datetime.desc()).limit(limit).all()

    @staticmethod
    def get_latest(db: Session, symbol: str) -> Optional[TickHistory]:
        """最新のティックデータを取得"""
        return db.query(TickHistory) \
            .filter(TickHistory.symbol == symbol) \
            .order_by(TickHistory.tick_datetime.desc()) \
            .first()
