from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class DocumentSchema(BaseModel):
    content: str
    topic: str


class DocumentPublic(BaseModel):
    id: int
    content: str
    topic: str
    owner_id: int


class DocumentList(BaseModel):
    documents: list[DocumentPublic]


class DocumentUpdate(BaseModel):
    content: str | None = None
    topic: str | None = None


#fazendo
class CollectionSchema(BaseModel):
    id: int
    name: str
    owner_id: int


class CreateCollectionSchema(BaseModel):
    name: str
    topic: str | None = None
    skip: int | None = 0
    limit: int | None = 100


class CollectionPublic(BaseModel):
    id: int
    name: str


class CollectionList(BaseModel):
    collections: list[CollectionPublic]


class QuestionModel(BaseModel):
    id_collection: int
    prompt: str

#class Topics(Basemodel)