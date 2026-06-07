from sqlalchemy import Column, String, DateTime
# sqlalchemy version of columns, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
# sqlalchemy version of UUID in postgreSQL
from database import Base
# is this like from the database.py ? declarative_base? 
import uuid
# python's version of creating UUID
from datetime import datetime
#python's version of creating utc timestamp

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # default is executed when it is not given 
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)