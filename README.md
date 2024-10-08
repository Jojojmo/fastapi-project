# Sobre o Projeto

Este projeto foi desenvolvido com base nas aulas do Eduardo Mendes, que você pode acessar [neste link](https://fastapidozero.dunossauro.com/).

O principal objetivo é facilitar a integração de bancos de dados vetoriais com o modelo LLama. Com isso, a aplicação permite:

- **Respostas Contextualizadas:** O modelo pode responder a perguntas baseadas no contexto de uma coleção de documentos, oferecendo informações mais relevantes e precisas.
- **Verificação de Similaridade:** É possível avaliar a similaridade entre perguntas e os dados armazenados, ajudando na identificação de relações e padrões.

# Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Rotas](#rotas)
  - [/users](#users)
  - [/documents](#documents)
  - [/collections](#collections)
  - [/guess](#guess)
  - [/auth](#auth)
- [Configuração (Set Up)](#configuração-set-up)
- [Como Rodar a API](#como-rodar-a-api)
- [Como Rodar os Testes](#como-rodar-os-testes)
- [Criando Migrações com Alembic](#criando-migrações-com-alembic)


## Rotas

### /users
A rota `/users` é responsável pela gestão dos usuários. Através dela, é possível cadastrar novos usuários, editar informações de usuários existentes, remover usuários do sistema e atualizar dados ou permissões conforme necessário.

### /documents
A rota `/documents` gerencia os arquivos de texto criados pelos usuários. Somente o usuário que criou um documento pode acessá-lo, garantindo a privacidade e a segurança das informações. Os usuários podem criar novos documentos e realizar operações de leitura e exclusão.

### /collections
A rota `/collections` organiza conjuntos de documentos no banco de dados. Cada coleção é associada a um vetor FAISS, que facilita buscas e análises de similaridade. Apenas o usuário que criou a coleção pode acessá-la, mantendo o controle sobre os dados.

### /guess
A rota `/guess` permite que os usuários façam perguntas relacionadas às coleções que criaram. O modelo LLama tenta responder com base no contexto dos documentos disponíveis, proporcionando uma consulta inteligente. Essa rota também avalia a similaridade entre as perguntas e os dados armazenados, ajudando os usuários a encontrar informações relevantes.

### /auth
A rota `/auth` é essencial para a segurança da aplicação, gerenciando a autenticação de usuários. Ela permite que apenas usuários autenticados acessem os recursos da API. Além disso, a rota facilita a atualização de tokens de autenticação, assegurando que as sessões dos usuários permaneçam ativas e seguras.


## Configuração (Set Up)

1. **Criar um Ambiente Virtual**:
   Abra o terminal e navegue até o diretório do seu projeto. Em seguida, execute:
   ```bash
   python -m venv venv
   ```
   Isso criará uma nova pasta chamada `venv` que contém o ambiente virtual.

2. **Ativar o Ambiente Virtual**:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS e Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Instalar Dependências**:
   Instale as bibliotecas necessárias, normalmente listadas em um arquivo `requirements.txt` (se houver):
   ```bash
   pip install -r requirements.txt
   ```

### Usando Poetry

1. **Instalar o Poetry**:
   Se você ainda não tem o Poetry instalado, você pode instalar usando o seguinte comando:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Ou, se estiver no Windows, você pode seguir as instruções no [site oficial do Poetry](https://python-poetry.org/docs/#installation).

2. **Criar um Novo Projeto (se necessário)**:
   Se você está criando um novo projeto, inicie um novo repositório com:
   ```bash
   poetry new fastapi_project
   ```

3. **Adicionar Dependências**:
   Navegue até o diretório do seu projeto e adicione as dependências necessárias. Caso tenha um `pyproject.toml`, você pode adicionar as dependências com:
   ```bash
   poetry install
   ```

4. **Ativar o Ambiente Poetry**:
   Para ativar o ambiente virtual criado pelo Poetry, use:
   ```bash
   poetry shell
   ```

### **Criar o Arquivo `.env`**:
   Semelhante ao método anterior, crie um arquivo `.env` na raiz do seu projeto e configure as variáveis de ambiente conforme indicado no arquivo `.envexample`.

### **Certifique-se da Versão Atualizada do LLama**:
   Por fim, garanta que você tenha uma versão atualizada do LLama. Você pode baixá-lo através do link fornecido: [aqui](https://ollama.com/).

## Como Rodar a API

Para iniciar a API, execute o seguinte comando:

```bash
uvicorn fastapi_project.app:app --reload
```

Acesse a documentação da API em:

[http://localhost:8000/docs](http://localhost:8000/docs)

## Como Rodar os Testes

Para executar os testes, utilize o comando:

```bash
pytest -s -x --cov=fastapi_project -vv
```

## Criando Migrações com Alembic

Para criar migrações no Alembic, use os seguintes comandos:

1. Para gerar uma nova migração:

   ```bash
   alembic revision --autogenerate -m "mensagem aqui"
   ```

2. Para aplicar as migrações:

   ```bash
   alembic upgrade head
   ```

