# Imports
import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from . import schemas, models, key_generator, crud
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from starlette.datastructures import URL
from .config import get_settings


# MAIN CODE

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LANDING PAGE
@app.get("/")
def read_root():
    return "Welcome to URL Shortener API"
# END LANDING PAGE


# RAISE
def raise_bad_request(msg):
    raise HTTPException(status_code=400, detail=msg)


def raise_not_found(req):
    msg = f"URL '{req.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=msg)

# END RAISE


# /URL PAGE
@app.post("/url", response_model=schemas.UrlInfo)
def generate_url(url: schemas.UrlBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("URL is not valid")
    db_url = crud.generate_db_url(db=db, url=url)
    return get_admin_info(db_url=db_url)
# END /URL PAGE


# /{URL_KEY} PAGE
def forward_to_target_url(url_key: str, req: Request, db: Session = Depends(get_db)):
    if db_url := crud.db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db, db_url)
        raise_not_found(req)
    return RedirectResponse(db_url.target_url)
# END /{URL_KEY} PAGE


# /admin/{secret_key} PAGE
@app.get('/admin/{secret_key}', name='admin info', response_model=schemas.UrlInfo)
def get_url_info(secret_key: str, req: Request, db: Session = Depends(get_db)):
    if db_url := crud.db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url=db_url)
    else:
        raise_not_found(req)


@app.delete('/admin/{secret_key}')
def delete_url(secret_key: str, req: Request, db: Session = Depends(get_db)):
    if db_url := crud.delete_db_url_by_secret_key(db, secret_key):
        msg = f'Successfully deleted shortened URL'
        return {'detail': msg}
    else:
        raise_not_found(req)
# END /admin/{secret_key} PAGE


def get_admin_info(db_url: models.Url):
    adm_endpoint = app.url_path_for("admin info", secret_key=db_url.secret_key)
    base_url = URL(get_settings().base_url)

    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=adm_endpoint))

    return db_url
