from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Numeric, select
from sqlalchemy.orm import relationship, Session
from typing import List
from database.base import Base
from models.base_model import BaseDAO

class TransactionModel(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    amount = Column(Numeric(10, 2), nullable=False)
    comment = Column(Text, nullable=True)

    # Foreign key
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category_rel = relationship('CategoryModel', back_populates='transactions')


class TransactionDAO(BaseDAO):
    def __init__(self):
        super().__init__(TransactionModel)

    def get_by_date_range(self, db: Session, start_date: datetime, end_date: datetime) -> List[TransactionModel]:
        query = select(TransactionModel).where(
            TransactionModel.date >= start_date,
            TransactionModel.date <= end_date
        )
        return list(db.execute(query).scalars().all())