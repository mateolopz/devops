from sqlalchemy import cast
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from src.db.models.blacklist import Blacklist

from src.db.schemas.blacklist import BlacklistEmail

from ..core.config.settings import Settings
settings = Settings()


def blacklist_email(db: Session, blacklist: BlacklistEmail):
    db_blacklist = Blacklist(**blacklist.dict())
    db.add(db_blacklist)
    db.commit()
    db.refresh(db_blacklist)
    return BlacklistEmail(email=db_blacklist.email, app_uuid=db_blacklist.app_uuid, blocked_reason=db_blacklist.blocked_reason)

def get_blacklist(db: Session, email: str):
    return db.query(Blacklist).filter(Blacklist.email == email).first()


