from subprocess import CalledProcessError
from fastapi import APIRouter, Depends
from fastapi import status, Response
from app_salt_keys.auth import get_api_key
from app_salt_keys.salt_keys import chek_keys_in_accepted
from app_salt_keys.salt_keys import key_accept
from app_salt_keys.salt_keys import key_delete


router = APIRouter(
    prefix="/api/v1",
    tags=["keys"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/keys/{key}", status_code=status.HTTP_200_OK)
def key_check(key: str, response: Response):
    try:
        if chek_keys_in_accepted(key) is True:
            return {"OK": key}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"ERROR": 'kye was not found'}
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"ERROR": 'Cannot run salt-kyes'}


@router.post("/keys/{key}", status_code=status.HTTP_201_CREATED)
def add_key(key: str, response: Response):
    try:
        key_accept(key)
        return {"OK": key}
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"ERROR": 'Cannot run salt-kyes'}


@router.delete("/keys/{key}", status_code=status.HTTP_200_OK)
def keys_delete(key: str, response: Response):
    try:
        key_delete(key)
        return {"OK": key}
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"ERROR": 'Cannot run salt-kyes'}
