from flask.cli import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int
    DEBUG_RESPONSE: bool

    USER: str
    PASSWORD: str
    HOST_NAME: str
    DB_NAME: str
    PORT: str

    REDIS_HOST_NAME: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    AUTO_CANCEL_SEC: int

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"

settings = Settings()
