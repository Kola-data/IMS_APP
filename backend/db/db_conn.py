
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)

try:
    
    AsyncSessionLocal = async_sessionmaker(
        bind=engine, 
        expire_on_commit=False
    )
    

    print("Database connection established successfully.")

except Exception as e:
    print(f"Error connecting to the database: {e}")


class Base(DeclarativeBase):
    pass


