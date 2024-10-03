from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_project.database import get_session
from fastapi_project.models import User
from fastapi_project.schemas import UserSchema, UserPublic, UserList, Message
from fastapi_project.security import get_password_hash, get_current_user



router = APIRouter(prefix='/users', tags=['users'])


#O annotated permite que possamos incluir metadados e informações
#dentro de uma anotação de tipo, ex: a: Annotated[int, '>10']
#A anotação T_ se refere a um "Tipo" segundo as PEP
T_Session =  Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User,Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, 
        password=get_password_hash(user.password), 
        email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session,
    skip: int = 0, 
    limit: int = 100, 
    ):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, 
    session: T_Session,
    current_user: T_CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                             detail='Not enough permission')

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, 
                session: T_Session,
                current_user: T_CurrentUser):
    
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                             detail='Not enough permission')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@router.get('/{user_id}', response_model=UserPublic)
def read_user__exercicio(user_id: int, session: T_Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user