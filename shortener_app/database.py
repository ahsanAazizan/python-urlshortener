import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

from .config import get_settings


engine = sqlalchemy.create_engine(get_settings().db_url, connect_args={"check_same_thread": False})
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.ext.declarative.declarative_base()
