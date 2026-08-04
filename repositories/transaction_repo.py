from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, select
import logging

from models.transactions import TransactionDAO, TransactionModel
from models.category import CategoryModel
from repositories.base_repo import BaseRepository
from exceptions import ValidationError, NotFoundError

logger = logging.getLogger(__name__)

class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(TransactionDAO())

    def create_transaction(self, db: Session, amount: float, date: datetime, category_id: int, comment: str = None) -> TransactionModel:
        if date is None:
            date = datetime.utcnow()

        if amount <= 0:
            raise ValidationError("Сумма должна быть больше 0")

        if date > datetime.utcnow():
            raise ValidationError("Дата не может быть в будущем")

        if category_id:
            category = db.get(CategoryModel, category_id)
            if not category:
                raise NotFoundError(f"Категория с id {category_id} не найдена")

        transaction_data = {
            'amount': amount,
            'date': date, 
            'category_id': category_id,
            'comment': comment
        }

        return self.create(db, transaction_data)

    def get_transactions_with_categories(self, db: Session, skip: int = 0, limit: int = 100):
        query = (
            select(TransactionModel)
            .options(joinedload(TransactionModel.category_rel))
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(query).scalars().all())

    def get_monthly_stat(self, db: Session, year: int, month: int):
        start_date = datetime(year, month, 1)
        end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
        
        total = (
            db.query(func.sum(TransactionModel.amount))
            .filter(TransactionModel.date >= start_date, TransactionModel.date < end_date)
            .scalar() or 0
        )

        count = (
            db.query(func.count(TransactionModel.id))
            .filter(TransactionModel.date >= start_date, TransactionModel.date < end_date)
            .scalar() or 0
        )

        return {'total': float(total), 'count': count}

    def get_monthly_stat_by_category(self, db: Session, year: int, month: int, category_id: int):
        start_date = datetime(year, month, 1)
        end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
        
        total = (
            db.query(func.sum(TransactionModel.amount))
            .filter(
                TransactionModel.date >= start_date, 
                TransactionModel.date < end_date,
                TransactionModel.category_id == category_id
            )
            .scalar() or 0
        )

        return total