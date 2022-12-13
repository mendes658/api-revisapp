from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_DAYS = settings.access_token_expire_days

def createAccessToken(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode['exp'] = expire

    encodedJwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encodedJwt

def verifyAccessToken(credentials_exception: str, token: Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = id
    except JWTError:
        raise credentials_exception
    
    return token_data



def getCurrentUser(token: str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    return verifyAccessToken(credentials_exception, token)