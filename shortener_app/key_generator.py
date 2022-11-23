from string import ascii_uppercase, digits
import secrets
from sqlalchemy.orm import Session
from . import crud


def generate_key(length):
    chars = ascii_uppercase + digits
    return ''.join(secrets.choice(chars) for i in range(length))


def generate_unique_key(db: Session):
    key = generate_key(length=5)
    while crud.db_url_by_key(db, key):
        key = generate_key(length=5)
    return key
