import uuid
from fastapi import APIRouter, Depends, Response, Header
from fastapi.responses import JSONResponse
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.db.schemas.blacklist import (
    BlacklistEmail,
    BlacklistReason,
)
import src.logic.blacklist as logic

router = APIRouter(
    prefix="/blacklists",
    tags=["blacklists"],
)

@router.post("/", response_model=BlacklistEmail, status_code=201)
def post_blacklist(email: BlacklistEmail, db: Session = Depends(get_db)):
    return logic.blacklist_email(db, email)

@router.get("/{email}", response_model=BlacklistReason, status_code=200)
def get_blacklist_by_email(email: str, db: Session = Depends(get_db)):
    blacklist = logic.get_blacklist(db, email)
    if not blacklist:
        return JSONResponse(content=False)
    return BlacklistReason(found=True, blocked_reason=blacklist.blocked_reason)