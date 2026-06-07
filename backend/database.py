from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Sets up  a convsersation with DB
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    # like return but does something  like clean up?? 
    finally:
        db.close() # even if exceptions arises it will close it

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.fetchone() #fetchone returns like in a (1,) just the 1