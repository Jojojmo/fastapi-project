from datetime import datetime, timedelta
from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_project.database import get_session
from fastapi_project.models import User
from fastapi_project.schemas import TokenData
from fastapi_project.settings import Settings

from sqlalchemy import select
from sqlalchemy.orm import Session


from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from jwt import decode,encode, ExpiredSignatureError
from jwt.exceptions import PyJWTError

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
settings =  Settings()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#SECRET_KEY foi Criado por secrets.token_hex(256) lib padrão do python


def create_access_token(payload_data: dict):
    to_encode = payload_data.copy()

    # Aciona um tempo de 30 minutos para expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    #Para ler o protocolo dos claims, arquivos que vão no payload do JWT, utilize o site:
    #https://www.iana.org/assignments/jwt/jwt.xhtml
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, 
                         algorithm=settings.ALGORITHM)

    return encoded_jwt



def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
    ):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, 
                         settings.SECRET_KEY, 
                         algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    
    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )
    if not user:
        raise credentials_exception
    return user



    #48mins ASSISTIR