import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_project.app import app
from fastapi_project.database import get_session
from fastapi_project.models import User, Document, Collection,table_registry
from fastapi_project.security import get_password_hash

import factory



class UserFactory(factory.Factory):
    class Meta:
        # Classe que será feita pelo Factory-Boy
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    # O lazy vai ser chamado depois dos métodos Eager "ansiosos", ou seja, nesse caso vai
    # construir o username e depois usar ele de base no email e password
    # Note que usamos `obj` como se fosse um self da variável que está sendo utilizada no factory
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class DocumentFactory(factory.Factory):
    class Meta:
        model = Document

    content = factory.Faker('text')
    topic = 'string'
    owner_id = 1


@pytest.fixture
def client(session):
    """
    Essa fixture faz o over ride do depens(get_session), ou seja,
    ela sobreescreve a Session para que possamos injetar nosso banco 
    de dados de teste que fica em memória (SQlite em Memória para testes)
    
    Params: Se não estiver enganado a propria session vem da nossa fixute session()
    """
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """
    Fixture que gera uma session no banco de dados em memória do Sqlite
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False}, # Ao gerar um bd no sqlite para testes, ele cria isso em thread's diferentes, o que dá conflito no sqlalchemy, para isso passamos o parametro como False
        poolclass=StaticPool, # Outro parametro por conta da checagem de thread's e limitações do sqlite dentro do sqlalchemy
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'testtest'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd #Monkey Patch

    return user

@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password}
    )
    return response.json()['access_token']


@pytest.fixture
def document(session, user):
    doc = Document(content='Assunto do dia', topic='teste', owner_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    return doc



from fastapi_project.vectors.embedding import (Save_vector, 
                                               create_collection,
                                               remove_collection)
import faiss

@pytest.fixture
def patch_save_vector_dir(monkeypatch):
    def mock_init(self, vector, name_file):
        self._Save_vector__d = 4096
        self._Save_vector__dir = 'tests/embeddings_test/'
        self.vector = vector
        self.name_file = name_file


    def mock_make_path(self):
        return self._Save_vector__dir + self.name_file


    def mock_save(self):
        path = self.make_path()
        index = faiss.IndexFlatL2(self._Save_vector__d)
        index.add(self.vector)
        faiss.write_index(index, path)


    monkeypatch.setattr(Save_vector, '__init__', mock_init)
    monkeypatch.setattr(Save_vector, 'make_path', mock_make_path)
    monkeypatch.setattr(Save_vector, 'save', mock_save)


@pytest.fixture
def documents_5(session, user):
    # Salva os documentos no banco
    session.bulk_save_objects(DocumentFactory.create_batch(5, owner_id=user.id))
    session.commit()

    # Busca os documentos recém-criados
    documents = session.query(Document).filter_by(owner_id=user.id).all()

    return documents


@pytest.fixture
def collection(session, user, documents_5):
    db_collection = Collection(name= 'string',
                               owner_id= user.id,
                               documents=documents_5)
    
    session.add(db_collection)
    session.commit()
    session.refresh(db_collection)


# import os

# @pytest.fixture
# def patch_remove_collection(monkeypatch):
#     def mock_remove_collection(name_file: str):
#         file_path = 'tests/embeddings_test/' + name_file + '.bin'

#         if os.path.exists(file_path):
#             os.remove(file_path)
    
#     monkeypatch.setattr('fastapi_project.vectors.embedding.remove_collection', mock_remove_collection)

