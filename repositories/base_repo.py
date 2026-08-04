from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from models.base_model import BaseDAO

class BaseRepository:
    def __init__(self, dao: BaseDAO):
        self.dao = dao

    def get_one(self, db: Session, id: int) -> Any:
        """Получить запись по ID."""
        return self.dao.get_one(db, id)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Получить список записей с пагинацией и фильтрами."""
        return self.dao.get_mult(db, skip, limit, filters)
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> Any:
        """Создать новую запись."""
        return self.dao.create(db, obj_in)
    
    def update(self, db: Session, id: int, obj_in: Dict[str, Any]) -> Any:
        """Обновить запись."""
        return self.dao.update(db, id, obj_in)
    
    def delete(self, db: Session, id: int) -> bool:
        """Удалить запись."""
        return self.dao.delete(db, id)