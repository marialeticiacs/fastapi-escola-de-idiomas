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

@pytest.fixture
def setup_data(client):
    client.post("escola/professores/", json={
        "nome": "Professor Teste",
        "cpf": "123.456.789-00",
        "email": "professor.teste@example.com",
        "data_nascimento": "1980-01-01"
    })

    client.post("escola/niveis/", json={
        "nome": "Nível Teste",
        "descricao": "Descrição do nível teste"
    })

    client.post("escola/disciplinas/", json={
        "nome": "Disciplinas Teste",
        "descricao": "Descrição da Disciplinas teste"
    })

    client.post("escola/salas/", json={
        "nome": "Sala Teste",
        "capacidade": 30
    })

    client.post("escola/alunos/", json={
        "nome": "Aluno Teste",
        "cpf": "987.654.321-00",
        "email": "aluno.teste@example.com",
        "dt_nascimento": "2000-01-01"
    })

    client.post("escola/cursos/", json={
        "nome": "Curso Teste",
        "id_professor": 1,
        "id_nivel": 1,
        "id_disciplinas": 1,
        "id_sala": 1,
        "descricao": "Descrição do curso teste",
        "data_inicio": "2023-01-01",
        "data_fim": "2023-12-31"
    })

def test_create_curso(client, setup_data):
    response = client.post("escola/cursos/", json={
        "nome": "Curso Teste",
        "id_professor": 1,
        "id_nivel": 1,
        "id_disciplinas": 1,
        "id_sala": 1,
        "descricao": "Descrição do curso teste",
        "data_inicio": "2023-01-01",
        "data_fim": "2023-12-31"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Curso Teste"
    assert response.json()["descricao"] == "Descrição do curso teste"
    assert response.json()["data_inicio"] == "2023-01-01"
    assert response.json()["data_fim"] == "2023-12-31"

def test_read_curso(client, setup_data):
    response = client.get("escola/cursos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Curso Teste"
    assert response.json()["descricao"] == "Descrição do curso teste"
    assert response.json()["data_inicio"] == "2023-01-01"
    assert response.json()["data_fim"] == "2023-12-31"

def test_update_curso(client, setup_data):
    response = client.put("escola/cursos/1", json={
        "nome": "Curso Atualizado",
        "descricao": "Descrição atualizada",
        "data_inicio": "2023-02-01",
        "data_fim": "2023-11-30"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Curso Atualizado"
    assert response.json()["descricao"] == "Descrição atualizada"
    assert response.json()["data_inicio"] == "2023-02-01"
    assert response.json()["data_fim"] == "2023-11-30"

