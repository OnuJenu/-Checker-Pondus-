from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create scoped session for thread safety
db = scoped_session(SessionLocal)

Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables"""
    # Import all models to ensure they're registered with Base
    from app.models.user import User
    from app.models.poll import Poll
    from app.models.vote import Vote
    from app.models.voting_option import VotingOption
    from app.models.media import Media
    
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    try:
        yield db
    finally:
        db.remove()
