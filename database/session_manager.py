from contextlib import contextmanager
from sqlalchemy.orm import Session
from database.connection import SessionLocal
import logging

logger = logging.getLogger(__name__)


@contextmanager
def get_db_session():
    """
    Контекстный менеджер для работы с сессией

    """

    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
        logger.info("Transaction committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Transaction rolled back: {str(e)}")
        raise
    finally:
        session.close()
        logger.debug("Session closed")