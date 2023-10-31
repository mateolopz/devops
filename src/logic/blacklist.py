from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from src.db.models.blacklist import Blacklist

from src.db.schemas.blacklist import BlacklistEmail
import re
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


def validate_email(email: str) -> bool:
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_regex.match(email))


def validate_uuid(uuid: str) -> bool:
    uuid_regex = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')
    return bool(uuid_regex.match(uuid))


def validate_host_ip(ip: str) -> bool:
    # TODO: Check if the client.host method returns IPv6 or IPv4
    ipv4_regex = re.compile(r'^[0-9]{3}.[0-9]{3}.[0-9]{3}.[0-9]{3}')

    # TODO: Buscar este regex, las reglas de IPv6 son mas particulares con lo de abreviaciones
    ipv6_regex = re.compile(r'^[0-9a-z]{4}:')
    # fe80::5149:7dc3:efd7:83cd%69

    ip_match = ipv4_regex.match(ip) or ipv6_regex.match(ip)
    return bool(ip_match)


def validate_blocked_description_length(s: str) -> bool:
    return len(s) <= 255
