from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class SolvedQuestion(Base):
    __tablename__ = "solved_questions"

    id         = Column(Integer, primary_key=True, index=True)
    question   = Column(Text, nullable=False, index=True)
    type       = Column(String(50), nullable=False)
    steps      = Column(JSON, nullable=False)
    answer     = Column(Text, nullable=False)
    source     = Column(String(20), default="engine")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
