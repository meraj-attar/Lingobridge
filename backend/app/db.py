import os
from sqlalchemy import create_engine, event
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).resolve().parents[1]/'.env')
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://lingobridge:lingobridge@localhost:5432/lingobridge')
kwargs = {'connect_args': {'check_same_thread': False}} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, **kwargs)
if DATABASE_URL.startswith('sqlite'):
    @event.listens_for(engine, 'connect')
    def fk_on(connection, _):
        connection.execute('PRAGMA foreign_keys=ON')
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db
