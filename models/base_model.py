from typing import TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.base import Base

ModelType = TypeVar('ModelType', bound=Base)

class BaseDAO:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_one(self, db: Session, id: int) -> Optional[ModelType]:
        """Получить одну запись в БД по ID."""
        return db.get(self.model, id)

    def get_mult(self, db: Session, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """Получить несколько записей в БД с фильтрами и пагинацией."""
        query = select(self.model)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

        query = query.offset(skip).limit(limit)
        result = db.execute(query)
        return list(result.scalars().all())

    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """Создать новую запись."""
        obj = self.model(**obj_in)
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def update(self, db: Session, id: int, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Обновить запись."""
        obj = self.get_one(db, id) # Исправлено с self.get на self.get_one
        
        if not obj:
            return None
        
        update_data = {
            field: value
            for field, value in obj_in.items()
            if hasattr(self.model, field) and value is not None
        }

        for field, value in update_data.items():
            setattr(obj, field, value)

        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        """Удалить запись."""
        obj = self.get_one(db, id) # Исправлено с self.get на self.get_one

        if not obj:
            return False
        
        db.delete(obj)
        db.flush()
        return True

    def exists(self, db: Session, **filters) -> bool:
        """Проверить наличие записей по фильтрам."""
        query = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = db.execute(query).scalar()
        return result is not None