
from fastapi import APIRouter, Depends, HTTPException


from fastapi_project.database import get_session
from fastapi_project.models import User, Collection, Document
from fastapi_project.security import get_current_user
from fastapi_project.schemas import (CollectionSchema,
                                     CollectionPublic, 
                                     CreateCollectionSchema,
                                     CollectionList,
                                     Message)
from fastapi_project.vectors.embedding import create_collection, remove_collection


from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session


T_Session =  Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("/", 
             status_code= HTTPStatus.CREATED,
             response_model=CollectionPublic)
def create_model(session: T_Session,
                 user: T_User,
                 collection: CreateCollectionSchema):
    name_exist = session.scalar(select(Collection).where(Collection.name == collection.name))
    if name_exist:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='This name already exists'
        )

    query = select(Document).where(Document.owner_id == user.id)
    if collection.topic:
        query = query.filter(Document.topic.contains(collection.topic))

    documents = session.scalars(query.offset(collection.skip).limit(collection.limit)).all()
    
    if len(documents) == 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The query returned no documents. Please check the query parameters or ensure tath the requested documents exist.'
        )
    create_collection(documents=documents,name=collection.name)
    db_collection = Collection(name=collection.name,
                               owner_id= user.id,
                               documents=documents)
    session.add(db_collection)
    session.commit()
    session.refresh(db_collection)

    return db_collection


@router.get("/", 
            status_code= HTTPStatus.OK,
            response_model= CollectionList)
def read_collections(session: T_Session,
                     user: T_User,
                     skip: int = 0,
                     limit: int = 100):
    query = select(Collection).where(Collection.owner_id == user.id)
    collections = session.scalars(query.offset(skip).limit(limit)).all()
    return {'collections': collections}


@router.put("/{collection_id}",
               response_model= CollectionPublic)
def update_model(
    collection_id: int,
    session: T_Session,
    user: T_User,
    collection: CreateCollectionSchema
    ):
    db_collection = session.scalar(
        select(Collection).where(Collection.owner_id == user.id,
                                 Collection.id == collection_id)
    )
    if not db_collection:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Collection not found"
        )
    name_exist = session.scalar(select(Collection).where(Collection.name == collection.name))
    if name_exist:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='This name already exists'
        )
    
    query = select(Document).where(Document.owner_id == user.id)
    if collection.topic:
        query = query.filter(Document.topic.contains(collection.topic))

    documents = session.scalars(query.offset(collection.skip).limit(collection.limit)).all()
    
    create_collection(documents=documents,name=collection.name)
    
    for key, value in collection.model_dump(exclude_unset=True).items(): 
        # model_dump transforma o schema em um "dicionario"
        # exclude_unset todos os dados que não vieram no schema (None), você não vai usar
        setattr(db_collection, key, value)

    session.add(db_collection)
    session.commit()
    session.refresh(db_collection)

    return db_collection


@router.delete("/{collection_id}", response_model= Message)
def delete_collection(collection_id, 
                      session: T_Session, 
                      user: T_User):
    db_collection = session.scalar(
        select(Collection).where(Collection.owner_id == user.id,Collection.id == collection_id)
    )

    if not db_collection:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Collection not found"
        )

    try:
        remove_collection(db_collection.name)
    except:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error in deleted"          
        )

    session.delete(db_collection)
    session.commit()

    return {'message': 'Collection deleted'}