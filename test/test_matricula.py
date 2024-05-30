from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database import Base, get_db
import pytest
from datetime import date

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
    # Criar professor
    client.post("escola/professores/", json={
        "nome": "Professor Teste",
        "cpf": "123.456.789-00",
        "email": "professor.teste@example.com",
        "data_nascimento": "1980-01-01"
    })

    # Criar nível
    client.post("escola/niveis/", json={
        "nome": "Nível Teste",
        "descricao": "Descrição do nível teste"
    })

    # Criar Disciplinas
    client.post("escola/disciplinas/", json={
        "nome": "Disciplina Teste",
        "descricao": "Descrição do Disciplina teste"
    })

    # Criar sala
    client.post("escola/salas/", json={
        "nome": "Sala Teste",
        "capacidade": 30
    })

    # Criar aluno
    client.post("escola/alunos/", json={
        "nome": "Aluno Teste",
        "cpf": "987.654.321-00",
        "email": "aluno.teste@example.com",
        "dt_nascimento": "2000-01-01"
    })

    # Criar curso
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


def test_create_matricula(client, setup_data):
    response = client.post("escola/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    assert response.status_code == 201
    assert response.json()["id_aluno"] == 1
    assert response.json()["id_curso"] == 1


def test_update_matricula(client, setup_data):
    client.post("escola/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    response = client.put("escola/matriculas/1", json={
        "data_matricula": "2024-05-15"
    })
    assert response.status_code == 200
    assert response.json()["data_matricula"] == "2024-05-15"

def test_delete_matricula(client, setup_data):
    client.post("escola/matriculas/", json={
        "id_aluno": 1,
        "id_curso": 1,
        "data_matricula": "2024-05-01"
    })
    response = client.delete("escola/matriculas/1")
    assert response.status_code == 200
    response = client.get("escola/matriculas/1")
    assert response.status_code == 404
