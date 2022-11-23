from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Url(Base):
    # Name of the table
    __tablename__ = "urls"

    # Table components
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
