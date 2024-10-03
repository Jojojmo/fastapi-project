if __name__ == '__main__':

    import sys
    import os
    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import Session

    # Adicionando o diretório anterior ao sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

    from fastapi_project.settings import Settings
    from fastapi_project.models import Document, Collection

    engine = create_engine(Settings().DATABASE_URL)


    from pprint import pprint

    with Session(engine) as session:
        res = session.scalar(select(Collection).where(Collection.id == 1))
        pprint(res.documents)
        print([doc.content for doc in res.documents])