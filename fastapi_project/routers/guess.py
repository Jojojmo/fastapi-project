from fastapi import APIRouter, Depends, HTTPException
from fastapi_project.database import get_session
from fastapi_project.models import User, Collection
from fastapi_project.security import get_current_user
from fastapi_project.schemas import QuestionModel, Message
from fastapi_project.vectors.call_llama import Call_llama


from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session


T_Session =  Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


router = APIRouter(prefix='/guess', tags=['guess'])


def decorator_model(func):
    def model(session: T_Session,
              user: T_User,
              question: QuestionModel):
        db_collection = session.scalar(
                            select(Collection)\
                            .where(Collection.id == question.id_collection,
                                Collection.owner_id == user.id))
        
        if not db_collection:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Collection not found"
            )


        documents = [doc.content for doc in db_collection.documents]

        model = Call_llama(name_collection = db_collection.name,
                        documents_list = documents)
        return func(model,question.prompt)
    return model

@router.post("/similarity", response_model= list)
@decorator_model
def guess_similarity(model, prompt):
    return model.similarity(prompt)


@router.post("/answer", response_model= Message)
@decorator_model
def guess_similarity(model, prompt):
    return {"message": model.answer(prompt)}


# @router.post("/similarity", response_model= list)
# def guess_similarity(session: T_Session,
#                      user: T_User,
#                      question: QuestionModel):
#     db_collection = session.scalar(
#                         select(Collection)\
#                         .where(Collection.id == question.id_collection,
#                                Collection.owner_id == user.id))
    
#     if not db_collection:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail="Collection not found"
#         )


#     documents = [doc.content for doc in db_collection.documents]

#     model = Call_llama(name_collection = db_collection.name,
#                        documents_list = documents)
    
#     return model.similarity(question.prompt)