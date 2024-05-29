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

def test_create_matricula(client):
    response = client.post("/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    assert response.status_code == 201
    assert response.json()["id_aluno"] == 1
    assert response.json()["id_curso"] == 1

def test_read_matricula(client):
    client.post("/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    response = client.get("/matriculas/1")
    assert response.status_code == 200
    assert response.json()["id_aluno"] == 1
    assert response.json()["id_curso"] == 1

def test_update_matricula(client):
    client.post("/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    response = client.put("/matriculas/1", json={
        "data_matricula": "2024-05-15"
    })
    assert response.status_code == 200
    assert response.json()["data_matricula"] == "2024-05-15"

def test_delete_matricula(client):
    client.post("/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    response = client.delete("/matriculas/1")
    assert response.status_code == 200
    response = client.get("/matriculas/1")
    assert response.status_code == 404
