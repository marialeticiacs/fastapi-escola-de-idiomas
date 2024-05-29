from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database import Base, get_db
import pytest

DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '123456'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_NAME = 'escola_idiomas' 

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_curso(client):
    response = client.post("/cursos/", json={
        "nome": "Inglês Básico",
        "id_professor": 1,
        "id_nivel": 1,
        "id_material": 1,
        "id_sala": 1,
        "descricao": "Curso de inglês para iniciantes",
        "data_inicio": "2024-06-01",
        "data_fim": "2024-12-01"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Inglês Básico"
    assert response.json()["descricao"] == "Curso de inglês para iniciantes"

def test_read_curso(client):
    client.post("/cursos/", json={
        "nome": "Inglês Básico",
        "id_professor": 1,
        "id_nivel": 1,
        "id_material": 1,
        "id_sala": 1,
        "descricao": "Curso de inglês para iniciantes",
        "data_inicio": "2024-06-01",
        "data_fim": "2024-12-01"
    })
    response = client.get("/cursos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Inglês Básico"
    assert response.json()["descricao"] == "Curso de inglês para iniciantes"

def test_update_curso(client):
    client.post("/cursos/", json={
        "nome": "Inglês Básico",
        "id_professor": 1,
        "id_nivel": 1,
        "id_material": 1,
        "id_sala": 1,
        "descricao": "Curso de inglês para iniciantes",
        "data_inicio": "2024-06-01",
        "data_fim": "2024-12-01"
    })
    response = client.put("/cursos/1", json={
        "descricao": "Curso de inglês básico para iniciantes"
    })
    assert response.status_code == 200
    assert response.json()["descricao"] == "Curso de inglês básico para iniciantes"

def test_delete_curso(client):
    client.post("/cursos/", json={
        "nome": "Inglês Básico",
        "id_professor": 1,
        "id_nivel": 1,
        "id_material": 1,
        "id_sala": 1,
        "descricao": "Curso de inglês para iniciantes",
        "data_inicio": "2024-06-01",
        "data_fim": "2024-12-01"
    })
    response = client.delete("/cursos/1")
    assert response.status_code == 200
    response = client.get("/cursos/1")
    assert response.status_code == 404

