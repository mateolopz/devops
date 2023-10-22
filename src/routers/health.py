from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.db.db import get_db


router = APIRouter(
    prefix="",
)

@router.get("/")
def ping():
    return "ping"

