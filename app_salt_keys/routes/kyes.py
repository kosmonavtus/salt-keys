from subprocess import CalledProcessError
from fastapi import APIRouter, Depends
from fastapi import status, Response
from app_salt_keys.auth import get_api_key
from app_salt_keys.salt_keys import key_accept
from app_salt_keys.salt_keys import key_accepted_check
from app_salt_keys.salt_keys import key_delete
from app_salt_keys.config import Settings


config = Settings()


router = APIRouter(
    prefix="/api/v1",
    tags=["keys"],
    dependencies=[Depends(get_api_key)],
)


@router.post("/keys/{key}", status_code=status.HTTP_201_CREATED)
def add_key(key: str, response: Response):
    try:
        key_accept(config.salt_worck_dir, key, config.bin_path)
        return {"OK": key}
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"ERROR": 'Cannot run salt-kyes'}


@router.get("/keys/{key}", status_code=status.HTTP_200_OK)
def key_check(key: str, response: Response):
    try:
        kyes_dict = key_accepted_check(config.salt_worck_dir, config.bin_path)
        if key in kyes_dict['minions']:
            return {"OK": key}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"ERROR": 'kye was not found'}
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"ERROR": 'Cannot run salt-kyes'}


@router.delete("/keys/{key}", status_code=status.HTTP_200_OK)
def keys_delete(key: str, response: Response):
    try:
        key_delete(config.salt_worck_dir, key, config.bin_path)
        return {"OK": key}
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"ERROR": 'Cannot run salt-kyes'}
