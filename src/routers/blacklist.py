from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.db.schemas.blacklist import (
    BlacklistEmail,
    BlacklistReason,
)
from fastapi_jwt_auth import AuthJWT
import src.logic.blacklist as logic

router = APIRouter(
    prefix="/blacklists",
    tags=["blacklists"],
)


@router.post("/", status_code=201)
def post_blacklist(email: BlacklistEmail, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    # authorize.create_access_token(subject=email.app_uuid, expires_time=False))
    authorize.jwt_required()
    blacklist = logic.blacklist_email(db, email)
    if not blacklist:
        raise HTTPException(status_code=404, detail="Email ya se encuentra registrado")
    return JSONResponse(content="Email agregado a la lista negra", status_code=201)


@router.get("/{email}", response_model=BlacklistReason, status_code=200)
def get_blacklist_by_email(email: str, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    blacklist = logic.get_blacklist(db, email)
    if not blacklist:
        return JSONResponse(content={"found": False}, status_code=404)
    return BlacklistReason(found=True, blocked_reason=blacklist.blocked_reason)
