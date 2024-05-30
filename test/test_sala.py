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

def test_create_sala(client):
    response = client.post("/escola/salas/", json={
        "nome": "Sala 101",
        "capacidade": 30
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Sala 101"
    assert response.json()["capacidade"] == 30

def test_read_sala(client):
    client.post("/escola/salas/", json={
        "nome": "Sala 101",
        "capacidade": 30
    })
    response = client.get("/escola/salas/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Sala 101"
    assert response.json()["capacidade"] == 30

def test_update_sala(client):
    client.post("/escola/salas/", json={
        "nome": "Sala 101",
        "capacidade": 30
    })
    response = client.put("/escola/salas/1", json={
        "nome": "Sala 102",
        "capacidade": 40
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Sala 102"
    assert response.json()["capacidade"] == 40

def test_partial_update_sala(client):
    client.post("/escola/salas/", json={
        "nome": "Sala 101",
        "capacidade": 30
    })
    response = client.put("/escola/salas/1", json={
        "capacidade": 40
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Sala 101"
    assert response.json()["capacidade"] == 40

def test_delete_sala(client):
    client.post("/escola/salas/", json={
        "nome": "Sala 101",
        "capacidade": 30
    })
    response = client.delete("/escola/salas/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Sala 101"
    assert response.json()["capacidade"] == 30

def test_create_sala(client):
    response = client.post("/escola/salas/", json={
        "nome": "Sala 101",
        "capacidade": 30
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Sala 101"
    assert response.json()["capacidade"] == 30
