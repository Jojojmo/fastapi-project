TODO's

[X] Criar BD
 - [X] Schema Users
 - [X] Schema Documents

[ ] Autenticação

[ ] Inserir dados no banco FAISS
[ ] Permanencia dos dados no banco FAISS

[ ] Endpoints
 - [X] Get user range
 - [X] Get user by id
 - [X] Create user
 - [X] Update user
 - [X] Delete user
 - [X] Get all documents
 - [ ] Get document by id
 - [X] Create document
 - [X] Update document
 - [X] Delete document
 - [ ] Make a Guess
 - [ ] ENDPOINT auth??


Como rodar a api:

```bash
uvicorn fastapi_project.app:app --reload
```


Como rodar os testes:

```bash
pytest -s -x --cov=fastapi_project -vv
```


Criando migrações no Alembic:

```bash
alembic revision --autogenerate -m "mensage here"
```

```bash
alembic upgrade head
```