from sqlalchemy.orm import Session
from repository import matricula_repository
from domain import schemas

def get_matricula(db: Session, matricula_id: int):
    return matricula_repository.get_matricula(db, matricula_id)

def get_matriculas(db: Session, skip: int = 0, limit: int = 10):
    return matricula_repository.get_matriculas(db, skip, limit)

def create_matricula(db: Session, matricula: schemas.MatriculaCreate):
    return matricula_repository.create_matricula(db, matricula)

def update_matricula(db: Session, matricula_id: int, matricula: schemas.MatriculaUpdate):
    return matricula_repository.update_matricula(db, matricula_id, matricula)

def delete_matricula(db: Session, matricula_id: int):
    return matricula_repository.delete_matricula(db, matricula_id)
