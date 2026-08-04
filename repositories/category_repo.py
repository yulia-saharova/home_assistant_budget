from sqlalchemy.orm import Session
from models.category import CategoryDAO
from repositories.base_repo import BaseRepository
from exceptions import ValidationError

class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(CategoryDAO())

    def get_all_categories(self, db: Session):
        return self.get_multi(db)

    def get_category_by_name(self, db: Session, name: str):
        return self.dao.get_by_name(db, name)

    def get_categories_by_type(self, db: Session, type_: str):
        return self.dao.get_by_type(db, type_)

    def create_category(self, db: Session, name: str, type_: str = None, description: str = None):
        """Создать категорию с валидацией."""
        existing = self.get_category_by_name(db, name)
        if existing:
            raise ValidationError(f"Категория {name} уже существует")

        category_data = {
            'name_category': name,
            'type_category': type_, 
            'description': description
        }

        return self.create(db, category_data)