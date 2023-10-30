from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from src.db.models.blacklist import Blacklist

from src.db.schemas.blacklist import BlacklistEmail

from ..core.config.settings import Settings
from sqlalchemy.exc import IntegrityError

settings = Settings()


def blacklist_email(db: Session, blacklist: BlacklistEmail):
    db_blacklist = Blacklist(**blacklist.dict())
    db.add(db_blacklist)
    try:
        db.commit()
        db.refresh(db_blacklist)
        return db_blacklist
    except IntegrityError:
        db.rollback()
        return


def get_blacklist(db: Session, email: str):
    return db.query(Blacklist).filter(Blacklist.email == email).first()
