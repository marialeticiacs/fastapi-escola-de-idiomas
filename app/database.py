import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '123456'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_NAME = 'escola_idiomas'
DATABASE_TEST_NAME = 'escola_idiomas_teste'

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
DATABASE_TEST_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_TEST_NAME}"

def create_database_if_not_exists(database_name):
    connection = None
    try:
        connection = psycopg2.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database="postgres"  
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Banco de dados '{database_name}' criado com sucesso!")
        else:
            print(f"Banco de dados '{database_name}' já existe.")
    except Exception as e:
        print(f"Erro ao verificar/criar o banco de dados: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

create_database_if_not_exists(DATABASE_NAME)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print("Conexão estabelecida com sucesso!")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

create_database_if_not_exists(DATABASE_TEST_NAME)

test_engine = create_engine(DATABASE_TEST_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

print("Banco de dados de teste configurado com sucesso!")
