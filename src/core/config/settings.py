import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_NAME: str = os.getenv("RDS_DB_NAME")
    DB_USER: str = os.getenv("RDS_USERNAME")
    DB_PASSWORD: str = os.getenv("RDS_PASSWORD")
    DB_HOST: str = os.getenv("RDS_HOSTNAME")
    DB_PORT: str = os.getenv("RDS_PORT")

class AuthSettings(BaseSettings):
    authjwt_secret_key:str = os.getenv('AUTHJWT_SECRET_KEY')

    class Config:
        case_sensitive = True


settings = Settings()
