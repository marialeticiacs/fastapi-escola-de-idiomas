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

def test_create_material(client):
    response = client.post("/escola/materiais/", json={
        "nome": "Livro de Inglês",
        "descricao": "Livro para nível básico"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Livro de Inglês"
    assert response.json()["descricao"] == "Livro para nível básico"

def test_read_material(client):
    client.post("/escola/materiais/", json={
        "nome": "Livro de Inglês",
        "descricao": "Livro para nível básico"
    })
    response = client.get("/escola/materiais/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Livro de Inglês"
    assert response.json()["descricao"] == "Livro para nível básico"

def test_update_material(client):
    client.post("/escola/materiais/", json={
        "nome": "Livro de Inglês",
        "descricao": "Livro para nível básico"
    })
    response = client.put("/escola/materiais/1", json={
        "nome": "Livro de Espanhol",
        "descricao": "Livro para nível intermediário"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Livro de Espanhol"
    assert response.json()["descricao"] == "Livro para nível intermediário"

def test_partial_update_material(client):
    client.post("/escola/materiais/", json={
        "nome": "Livro de Inglês",
        "descricao": "Livro para nível básico"
    })
    response = client.put("/escola/materiais/1", json={
        "descricao": "Livro para nível avançado"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Livro de Inglês"
    assert response.json()["descricao"] == "Livro para nível avançado"

def test_delete_material(client):
    client.post("/escola/materiais/", json={
        "nome": "Livro de Inglês",
        "descricao": "Livro para nível básico"
    })
    response = client.delete("/escola/materiais/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Livro de Inglês"
    assert response.json()["descricao"] == "Livro para nível básico"
