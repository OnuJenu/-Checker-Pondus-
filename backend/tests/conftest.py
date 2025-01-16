import pytest
from sqlalchemy import text
from app import create_app
from app.databases.database import db, Base
from app.config import TestConfig

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def test_db(app):
    """Create a new database for testing."""
    with app.app_context():
        from app.databases.database import init_db
        init_db()
        yield db

@pytest.fixture
def clean_db(app):
    """Clear the database before each test."""
    with app.app_context():
        # Reflect the database tables into metadata if not already loaded
        if not Base.metadata.tables:
            Base.metadata.reflect(bind=db.get_bind())
        
        # Truncate each table in reverse order to respect foreign key constraints
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f"DELETE FROM {table.name}"))
                
        db.commit()
        yield

        # Ensure session is clean after test
        db.remove()
