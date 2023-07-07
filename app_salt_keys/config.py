from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    API_KEY: str = "my file key"

    class Config:
        env_file = ".env"
