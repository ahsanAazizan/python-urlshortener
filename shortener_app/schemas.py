from pydantic import BaseModel


# URL Base
class UrlBase(BaseModel):
    target_url: str


class Url(UrlBase):
    active: bool
    clicks: int

    class Config:
        orm_mode = True


class UrlInfo(Url):
    url: str
    admin_url: str
