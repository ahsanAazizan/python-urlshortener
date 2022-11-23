from sqlalchemy.orm import Session
from . import key_generator, models, schemas


def generate_db_url(db: Session, url: schemas.UrlBase):
    key = key_generator.generate_unique_key(db)
    secret_key = f'{key}_{key_generator.generate_key(length=8)}'

    db_url = models.Url(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def db_url_by_key(db: Session, url_key: str):
    return db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()


def db_url_by_secret_key(db: Session, secret_key: str):
    return db.query(models.URL).filter(models.URL.secret_key == secret_key, models.URL.is_active).first()


def update_db_clicks(db: Session, db_url: schemas.Url):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def delete_db_url_by_secret_key(db: Session, secret_key: str):
    db_url = db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.active = False
        db.commit()
        db.refresh(db_url)
    return db_url



