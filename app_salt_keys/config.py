from typing import Dict, Any
from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


def GunicornSettings() -> Dict[str, Any]:
    return {
        'bind': '127.0.0.1:8008',
        'workers': 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'accesslog': 'access-salt-kyes-api.log',
        'errorlog': 'error-salt-kyes-api.log',
    }


class Settings(BaseSettings):
    api_key: str = "iechatheing8ahs4gohth2nie0ooJu2eeloo1xaiSh1fiengaiN2yoh7oowaheeb"
    salt_worck_dir: str = "/opt/saltstack/salt/"
    bin_path: str = "/opt/saltstack/salt/salt-key"

    class Config:
        env_file = ".env"
