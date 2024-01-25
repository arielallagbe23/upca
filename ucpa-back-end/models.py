from sqlalchemy import Column, Integer, String, Float, DateTime, func
from datetime import datetime
from database import Base

class PolishCalcul(Base):
    __tablename__ = 'polishcalculs'

    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String(100))
    result = Column(Float)
    timestamp = Column(DateTime, default=func.now())
