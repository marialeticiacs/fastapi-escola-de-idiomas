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
DATABASE_NAME = 'escola_idiomas_teste' 

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

def test_create_nivel(client):
    response = client.post("/escola/niveis/", json={
        "nome": "Básico",
        "descricao": "Nível básico de proficiência"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Básico"
    assert response.json()["descricao"] == "Nível básico de proficiência"

def test_read_nivel(client):
    client.post("/escola/niveis/", json={
        "nome": "Básico",
        "descricao": "Nível básico de proficiência"
    })
    response = client.get("/escola/niveis/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Básico"
    assert response.json()["descricao"] == "Nível básico de proficiência"

def test_update_nivel_partial(client):
    client.post("/escola/niveis/", json={
        "nome": "Básico",
        "descricao": "Nível básico de proficiência"
    })
    response = client.put("/escola/niveis/1", json={
        "descricao": "Nível intermediário de proficiência"
    })
    assert response.status_code == 200
    assert response.json()["descricao"] == "Nível intermediário de proficiência"

def test_delete_nivel(client):
    client.post("/escola/niveis/", json={
        "nome": "Básico",
        "descricao": "Nível básico de proficiência"
    })
    response = client.delete("/escola/niveis/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Básico"

def test_create_nivel(client):
    response = client.post("/escola/niveis/", json={
        "nome": "Básico",
        "descricao": "Nível básico de proficiência"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Básico"
    assert response.json()["descricao"] == "Nível básico de proficiência"
