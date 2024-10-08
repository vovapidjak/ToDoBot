from sqlalchemy import create_engine, Column, Integer, String
from app.database import Base


class TaskTable(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

