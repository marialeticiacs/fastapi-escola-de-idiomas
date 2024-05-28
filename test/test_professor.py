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

def test_create_professor(client):
    response = client.post("/escola/professores/", json={
        "nome": "Test Professor",
        "cpf": "123.456.789-00",
        "email": "test.professor@example.com",
        "data_nascimento": "1980-01-01"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Test Professor"
    assert response.json()["cpf"] == "123.456.789-00"
    assert response.json()["email"] == "test.professor@example.com"
    assert response.json()["data_nascimento"] == "1980-01-01"

def test_read_professor(client):
    client.post("/escola/professores/", json={
        "nome": "Test Professor",
        "cpf": "123.456.789-00",
        "email": "test.professor@example.com",
        "data_nascimento": "1980-01-01"
    })
    response = client.get("/escola/professores/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Test Professor"
    assert response.json()["cpf"] == "123.456.789-00"
    assert response.json()["email"] == "test.professor@example.com"
    assert response.json()["data_nascimento"] == "1980-01-01"

def test_update_professor(client):
    client.post("/escola/professores/", json={
        "nome": "Test Professor",
        "cpf": "123.456.789-00",
        "email": "test.professor@example.com",
        "data_nascimento": "1980-01-01"
    })
    response = client.put("/escola/professores/1", json={
        "nome": "Updated Professor"
    })
    response = client.post("/api/v1/professores/", json={"nome": "Test Professor"})
    assert response.status_code == 201
    assert response.json()["nome"] == "Test Professor"

def test_read_professor(client):
    client.post("/api/v1/professores/", json={"nome": "Test Professor"})
    response = client.get("/api/v1/professores/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Test Professor"

def test_update_professor(client):
    client.post("/api/v1/professores/", json={"nome": "Test Professor"})
    response = client.put("/api/v1/professores/1", json={"nome": "Updated Professor"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Updated Professor"

def test_delete_professor(client):
    client.post("/escola/professores/", json={
        "nome": "Ana Teste",
        "cpf": "123.456.789-01",
        "email": "ana.teste@example.com",
        "data_nascimento": "1990-02-02"
    })
    response = client.delete("/escola/professores/1")
    client.post("/api/v1/professores/", json={"nome": "Ana Teste"})
    response = client.delete("/api/v1/professores/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Ana Teste"
