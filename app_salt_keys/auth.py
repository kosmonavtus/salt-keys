from app_salt_keys.config import Settings
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN


config = Settings()


api_key_header = APIKeyHeader(name="access_token", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)) -> bool:
    if api_key_header == config.api_key:
        return True
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
