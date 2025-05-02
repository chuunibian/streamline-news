
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

DATABASE_URL = ""

engine = create_engine(DATABASE_URL) # create it

Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True)
#     username = Column(String(50), unique=True, nullable=False)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
#     conversations = relationship("Conversation", back_populates="user")

def init_db():
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

def get_db_session():
    Session = init_db()
    return Session()