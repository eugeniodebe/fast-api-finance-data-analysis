from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get and adjust DATABASE_URL for asyncpg
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Raise an error if DATABASE_URL is still not set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not properly configured.")

# Debugging line to confirm the modified URL
print(f"Adjusted DATABASE_URL: {DATABASE_URL}")

# Create the SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency for getting the database session
async def get_db():
    async with async_session_maker() as session:
        yield session