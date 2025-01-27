from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer, nullable=False)  # Ensure this field exists
    deadline = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, nullable=False)  # Associate task with a user
