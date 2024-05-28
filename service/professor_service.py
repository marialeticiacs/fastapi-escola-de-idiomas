from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository import professor_repository
from domain import schemas

def get_professor(db: Session, professor_id: int):
    professor = professor_repository.get_professor(db, professor_id)
    if professor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
    return professor

def get_professors(db: Session, skip: int = 0, limit: int = 10):
    return professor_repository.get_professors(db, skip, limit)

def create_professor(db: Session, professor: schemas.ProfessorCreate):
    return professor_repository.create_professor(db, professor)

def update_professor(db: Session, professor_id: int, professor: schemas.ProfessorCreate):
    db_professor = professor_repository.get_professor(db, professor_id)
    if db_professor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
    
    update_data = professor.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_professor, key, value)
    
    return professor_repository.update_professor(db, db_professor)

def delete_professor(db: Session, professor_id: int):
    db_professor = professor_repository.get_professor(db, professor_id)
    if db_professor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
    return professor_repository.delete_professor(db, professor_id)
