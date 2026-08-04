from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from config import settings

# Движок с очередью
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_recycle=settings.POOL_RECYCLE,
    echo=settings.ECHO_SQL,
    echo_pool="debug",
)



SessionLocal = sessionmaker(
    autocommit=False,  # изменения не будут сохраняться автоматически
    autoflush=False,  # не отправлять изменения перед каждым запросом
    bind=engine,
    expire_on_commit=False 
)