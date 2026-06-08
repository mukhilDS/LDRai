from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
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

class Couple(Base):
    __tablename__ = "couples"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invite_code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CoupleMember(Base):
    __tablename__ = "couple_members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    couple_id = Column(UUID(as_uuid=True), ForeignKey("couples.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    couple_id = Column(UUID(as_uuid=True), ForeignKey("couples.id"), nullable=False)
    mood = Column(Integer, nullable=False)
    stress = Column(Integer, nullable=False)
    miss_you = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)