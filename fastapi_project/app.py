from fastapi import FastAPI
from fastapi_project.routers import (auth, 
                                     collection, 
                                     documents, 
                                     users,
                                     guess)


app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(collection.router)
app.include_router(guess.router)




#uvicorn fastapi_project.app:app --reload