from bot import env
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(f"sqlite:///{env('DATABASE_NAME')}")
session = Session(bind=engine)
