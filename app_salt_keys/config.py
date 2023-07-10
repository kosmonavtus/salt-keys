from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    api_key: str = "iechatheing8ahs4gohth2nie0ooJu2eeloo1xaiSh1fiengaiN2yoh7oowaheeb"
    salt_worck_dir: str = "/opt/saltstack/salt"

    class Config:
        env_file = ".env"
