from sqlalchemy.orm import Session
from repository import curso_repository
from domain import schemas

def get_curso(db: Session, curso_id: int):
    return curso_repository.get_curso(db, curso_id)

def get_cursos(db: Session, skip: int = 0, limit: int = 10):
    return curso_repository.get_cursos(db, skip, limit)

def create_curso(db: Session, curso: schemas.CursoCreate):
    return curso_repository.create_curso(db, curso)

def update_curso(db: Session, curso_id: int, curso: schemas.CursoUpdate):
    return curso_repository.update_curso(db, curso_id, curso)

def delete_curso(db: Session, curso_id: int):
    return curso_repository.delete_curso(db, curso_id)
