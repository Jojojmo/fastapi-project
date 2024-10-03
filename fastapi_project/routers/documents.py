from fastapi import APIRouter, Depends, HTTPException

from fastapi_project.database import get_session
from fastapi_project.models import Document, User
from fastapi_project.schemas import (DocumentSchema,
                                     DocumentPublic,
                                     DocumentUpdate, 
                                     DocumentList,
                                     Message)
from fastapi_project.security import get_current_user

from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

T_Session =  Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/documents', tags=["documents"])


@router.post("/",
         status_code= HTTPStatus.CREATED,
         response_model=DocumentPublic)
def create_document(document:DocumentSchema, 
                    session: T_Session, 
                    user: T_User):
    db_document = Document(content=document.content, 
                           topic=document.topic, 
                           owner_id= user.id)
    session.add(db_document)
    session.commit()
    session.refresh(db_document)

    return db_document


@router.get("/",
         status_code=HTTPStatus.OK,
         response_model=DocumentList)
def read_documents(session: T_Session,
                   user: T_User, 
                   topic: str = None, 
                   skip: int = 0, 
                   limit: int = 100):
    
    query = select(Document).where(Document.owner_id == user.id)
    if topic:
        query = query.filter(Document.topic.contains(topic))

    documents = session.scalars(query.offset(skip).limit(limit)).all()
    return {'documents': documents}


@router.patch("/{document_id}", 
              response_model=DocumentPublic)
def update_document(document_id, 
                    session: T_Session,
                    user: T_User,
                    document: DocumentUpdate):
    db_document = session.scalar(
        select(Document).where(Document.owner_id == user.id,
                               Document.id == document_id)
    )
    if not db_document:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Document not found"
        )

    for key, value in document.model_dump(exclude_unset=True).items(): 
        # model_dump transforma o schema em um "dicionario"
        # exclude_unset todos os dados que não vieram no schema (None), você não vai usar
        setattr(db_document, key, value)

    session.add(db_document)
    session.commit()
    session.refresh(db_document)

    return db_document


@router.delete("/{document_id}", response_model= Message)
def delete_document(document_id, session: T_Session, user: T_User):
    db_document = session.scalar(
        select(Document).where(Document.owner_id == user.id,Document.id == document_id)
    )

    if not db_document:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Document not found"
        )

    session.delete(db_document)
    session.commit()

    return {'message': 'Document deleted'}


# add line

# remove line