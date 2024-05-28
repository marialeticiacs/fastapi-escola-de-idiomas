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

def test_create_aluno(client):
    response = client.post("/escola/alunos/", json={
        "nome": "Test Aluno",
        "cpf": "123.456.789-00",
        "email": "test.aluno@example.com",
        "dt_nascimento": "2000-01-01"
    })
    assert response.status_code == 201
    assert response.json()["nome"] == "Test Aluno"
    assert response.json()["cpf"] == "123.456.789-00"
    assert response.json()["email"] == "test.aluno@example.com"
    assert response.json()["dt_nascimento"] == "2000-01-01"

def test_read_aluno(client):
    client.post("/escola/alunos/", json={
        "nome": "Test Aluno",
        "cpf": "123.456.789-00",
        "email": "test.aluno@example.com",
        "dt_nascimento": "2000-01-01"
    })
    response = client.get("/escola/alunos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Test Aluno"
    assert response.json()["cpf"] == "123.456.789-00"
    assert response.json()["email"] == "test.aluno@example.com"
    assert response.json()["dt_nascimento"] == "2000-01-01"

def test_update_aluno(client):
    client.post("/escola/alunos/", json={
        "nome": "Test Aluno",
        "cpf": "123.456.789-00",
        "email": "test.aluno@example.com",
        "dt_nascimento": "2000-01-01"
    })
    response = client.put("/escola/alunos/1", json={
        "nome": "Updated Aluno"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Updated Aluno"
    assert response.json()["cpf"] == "123.456.789-00"  
    assert response.json()["email"] == "test.aluno@example.com"
    assert response.json()["dt_nascimento"] == "2000-01-01"

def test_partial_update_aluno(client):
    client.post("/escola/alunos/", json={
        "nome": "Test Aluno",
        "cpf": "123.456.789-00",
        "email": "test.aluno@example.com",
        "dt_nascimento": "2000-01-01"
    })
    response = client.put("/escola/alunos/1", json={
        "email": "updated.aluno@example.com"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Test Aluno"
    assert response.json()["cpf"] == "123.456.789-00"
    assert response.json()["email"] == "updated.aluno@example.com"
    assert response.json()["dt_nascimento"] == "2000-01-01"

def test_delete_aluno(client):
    client.post("/escola/alunos/", json={
        "nome": "Ana Teste",
        "cpf": "123.456.789-01",
        "email": "ana.teste@example.com",
        "dt_nascimento": "1990-02-02"
    })
    response = client.delete("/escola/alunos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Ana Teste"
