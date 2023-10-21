from fastapi import FastAPI
from src.db.db import engine
from src.db.db import Base
from src.routers import blacklist
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(status_code=400)


app.include_router(blacklist.router)
