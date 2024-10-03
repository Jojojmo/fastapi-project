from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_project.database import get_session
from fastapi_project.models import User
from fastapi_project.schemas import Token
from fastapi_project.security import (create_access_token,
                                      get_current_user, 
                                      verify_password)

from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session =  Annotated[Session, Depends(get_session)]
T_OAuth2From = Annotated[OAuth2PasswordRequestForm, Depends()] #O Depends vazio é para o tipo do OAuth ser respeitado e o Form funcionar no endpoint
T_User = Annotated[User, Depends(get_current_user)]

@router.post('/token', response_model= Token)
def login_for_access_token(
    form_data: T_OAuth2From, 
    session: T_Session
    ):
    user = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password'
        )

    access_token = create_access_token(payload_data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: T_User):
    new_access_token = create_access_token(payload_data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type':'bearer'}


