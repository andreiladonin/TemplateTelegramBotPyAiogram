from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from data.data import declarative_base, engine, session

Base = declarative_base()

def create_db():
    Base.metadata.create_all(engine)

class UserBot(Base):
    __tablename__ = 'UsersBot'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    message_count = Column(Integer)
    level = Column(String)
    date_created = Column(DateTime, default=datetime.now())

    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id
        self.level = "Новичок"
        self.message_count = 0





