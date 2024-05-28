from fastapi import FastAPI
from app.database import engine, Base
from controller import professor_controller, nivel_controller, aluno_controller


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Escola de Idiomas"}

app.include_router(professor_controller.router, prefix="/escola")
app.include_router(nivel_controller.router, prefix="/escola")
app.include_router(aluno_controller.router, prefix="/escola")
