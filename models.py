from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

# Подключение к базе данных (в данном случае SQLite)
DATABASE_URL = 'sqlite:///reminders.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель для сохранения уведомлений в базе данных
class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    reminder_datetime = Column(DateTime, default=func.now())
    
# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)
