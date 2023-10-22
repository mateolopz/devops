from fastapi import FastAPI
from src.db.db import engine
from src.db.db import Base
from src.routers import blacklist
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from fastapi import Request, status
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from src.core.config.settings import AuthSettings

Base.metadata.create_all(bind=engine)

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return AuthSettings()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(status_code=400)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message}
    )

app.include_router(blacklist.router)
