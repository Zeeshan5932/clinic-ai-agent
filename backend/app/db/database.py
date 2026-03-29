from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG, 
    future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def run_startup_migrations() -> None:
    """Apply lightweight, idempotent schema fixes for existing databases."""
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    if "appointments" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("appointments")}
    alter_statements = []

    if "email" not in columns:
        alter_statements.append("ALTER TABLE appointments ADD COLUMN email VARCHAR")
    if "notes" not in columns:
        alter_statements.append("ALTER TABLE appointments ADD COLUMN notes TEXT")
    if "google_event_id" not in columns:
        alter_statements.append("ALTER TABLE appointments ADD COLUMN google_event_id VARCHAR")
    if "status" not in columns:
        alter_statements.append("ALTER TABLE appointments ADD COLUMN status VARCHAR DEFAULT 'scheduled'")
    if "created_at" not in columns:
        alter_statements.append("ALTER TABLE appointments ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
    if "updated_at" not in columns:
        alter_statements.append("ALTER TABLE appointments ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP")

    if not alter_statements:
        return

    with engine.begin() as connection:
        for statement in alter_statements:
            connection.execute(text(statement))


def get_db():
    """Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
