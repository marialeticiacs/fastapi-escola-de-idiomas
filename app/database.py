import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '123456'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_NAME = 'escola_idiomas'
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

def create_database_if_not_exists():
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
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
            print(f"Banco de dados '{DATABASE_NAME}' criado com sucesso!")
        else:
            print(f"Banco de dados '{DATABASE_NAME}' já existe.")
    except Exception as e:
        print(f"Erro ao verificar/criar o banco de dados: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

create_database_if_not_exists()

print("DATABASE_URL: ", DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("Conexão estabelecida com sucesso!")
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
