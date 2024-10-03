
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