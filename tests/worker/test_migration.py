import pytest
import sqlite3
from migration import users, scripts, review_jobs  # Import tables
from sqlalchemy import create_engine, text

@pytest.fixture
def db_engine():
    engine = create_engine('sqlite:///:memory:', echo=False)
    from migration import metadata
    metadata.create_all(engine)
    return engine

def test_migration_tables(db_engine):
    conn = db_engine.connect()
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = [row[0] for row in result]
    assert 'users' in tables
    assert 'scripts' in tables
    assert 'review_jobs' in tables
    conn.close()

def test_admin_seed(db_engine):
    from migration import conn  # Simulate seed
    # Insert and query
    conn = db_engine.connect()
    conn.execute(text("INSERT INTO users (id, name, email, role) VALUES ('admin1', 'cbwinslow', 'blaine.winslow@gmail.com', 'admin')"))
    result = conn.execute(text("SELECT role FROM users WHERE email='blaine.winslow@gmail.com'"))
    assert result.fetchone()[0] == 'admin'
    conn.commit()
    conn.close()
