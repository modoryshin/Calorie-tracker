from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, status
import os
from dotenv import load_dotenv, find_dotenv

API_KEY_NAME = 'access_token'
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

load_dotenv(find_dotenv())

API_KEY = os.getenv('API_KEY')

async def get_api_key(api_key_header: str = Security(api_key_header)) -> str | None:
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No API Key detected')
        
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Could not validate credentials')
