from sqlalchemy import Column, Integer, String, Text, Float, select
from sqlalchemy.orm import relationship, Session
from typing import List, Optional
from models.base_model import BaseDAO
from database.base import Base

class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name_category = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    type_category = Column(String(20), nullable=False)
    month_limit = Column(Float, nullable=True)

    transactions = relationship('TransactionModel', back_populates='category_rel', lazy="select")


class CategoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(CategoryModel)

    def get_by_name(self, db: Session, name: str) -> Optional[CategoryModel]:
        query = select(CategoryModel).where(CategoryModel.name_category == name)
        return db.execute(query).scalar_one_or_none()

    def get_by_type(self, db: Session, type_: str) -> List[CategoryModel]:
        query = select(CategoryModel).where(CategoryModel.type_category == type_)
        return list(db.execute(query).scalars().all())