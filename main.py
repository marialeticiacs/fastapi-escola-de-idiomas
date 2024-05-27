from fastapi import FastAPI
from app.database import engine, Base
from controller import professor_controller, material_controller, sala_controller

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Escola de Idiomas"}

app.include_router(professor_controller.router, prefix="/escola")
app.include_router(sala_controller.router, prefix="/escola")
app.include_router(material_controller.router, prefix="/escola")
