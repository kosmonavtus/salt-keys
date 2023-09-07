from subprocess import CalledProcessError
from fastapi import APIRouter, Depends
from fastapi import status, Response
from app_salt_keys.auth import get_api_key
from app_salt_keys.salt_keys import chek_keys_in_accepted
from app_salt_keys.salt_keys import chek_keys_in_unaccepted
from app_salt_keys.salt_keys import key_accept
from app_salt_keys.salt_keys import key_delete
from pydantic import BaseModel


class State_status(BaseModel):
    state: str = 'ok'


router = APIRouter(
    prefix="/api/v1",
    tags=["keys"],
    dependencies=[Depends(get_api_key)]
)


@router.get("/keys/{key}", status_code=status.HTTP_200_OK, response_model=State_status)
def key_check(key: str, response: Response) -> State_status:
    try:
        if chek_keys_in_accepted(key) is True:
            response.headers["Content-Type"] = "application/json"
            state = State_status(state='ok')
            return state
        elif chek_keys_in_unaccepted(key) is False:
            response.status_code = status.HTTP_204_NO_CONTENT
            response.headers["Content-Type"] = "application/json"
            state = State_status(state='key was not found in unaccepted keys try again later')
            return state
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.headers["Content-Type"] = "application/json"
            state = State_status(state='key was not found in accepted and unaccepted keys')
            return state
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.headers["Content-Type"] = "application/json"
        state = State_status(state='Cannot run salt-kyes')
        return state


@router.post("/keys/{key}", status_code=status.HTTP_201_CREATED, response_model=State_status)
def add_key(key: str, response: Response) -> State_status:
    try:
        if chek_keys_in_accepted(key) is True:
            response.status_code = status.HTTP_200_OK
            response.headers["Content-Type"] = "application/json"
            state = State_status(state='ok')
            return state
        elif chek_keys_in_accepted(key) is False:
            if key_accept(key) is True:
                response.status_code = status.HTTP_201_CREATED
                state = State_status(state='ok')
                return state
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
                state = State_status(state=f'The key glob {key} does not match any unaccepted keys.')
                return state 
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.headers["Content-Type"] = "application/json"
            state = State_status(state='kye was not found in accepted keys')
            return state
    except(CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.headers["Content-Type"] = "application/json"
        state = State_status(state='Cannot run salt-kyes')
        return state
    except:
        state = State_status(state='Unknown error')
        response.headers["Content-Type"] = "application/json"
        return state


@router.delete("/keys/{key}", status_code=status.HTTP_200_OK, response_model=State_status)
def keys_delete(key: str, response: Response) -> State_status:
    try:
        key_delete(key)
        response.headers["Content-Type"] = "application/json"
        state = State_status(state='ok')
        return state
    except (CalledProcessError, FileNotFoundError, PermissionError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        state = State_status(state='Cannot run salt-kyes')
        response.headers["Content-Type"] = "application/json"
        return state
    

'''
1) Проверям что ключ в принятых - если ключ там есть то возращаем ок
2) Если ключа нет в принятых - провряем есть ли ключ  в НЕпринятых.
   Если ключа нет в не принятых вовзращем - 204.
3) Если ключа нет в принятых и ключ есть в НЕ приянытх  - вовзвращаем 404. 
'''