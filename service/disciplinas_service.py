from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository import disciplinas_repository
from domain import schemas, models

def get_disciplina(db: Session, disciplinas_id: int):
    disciplinas = disciplinas_repository.get_disciplina(db, disciplinas_id)
    if disciplinas is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina não encontrado")
    return disciplinas

def get_disciplinas(db: Session, skip: int = 0, limit: int = 10):
    return disciplinas_repository.get_disciplinas(db, skip, limit)

def create_disciplinas(db: Session, disciplinas: schemas.DisciplinasCreate):
    db_disciplinas = models.Disciplinas(**disciplinas.model_dump())
    return disciplinas_repository.create_disciplinas(db, db_disciplinas)

def update_disciplinas(db: Session, disciplinas_id: int, disciplinas: schemas.DisciplinasUpdate):
    db_disciplinas = disciplinas_repository.get_disciplina(db, disciplinas_id)
    if db_disciplinas is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplinas não encontrado")
    
    update_data = disciplinas.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_disciplinas, key, value)
    
    return disciplinas_repository.update_disciplinas(db, db_disciplinas)

def delete_disciplinas(db: Session, disciplinas_id: int):
    db_disciplinas = disciplinas_repository.get_disciplina(db, disciplinas_id)
    if db_disciplinas is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplinas não encontrado")
    return disciplinas_repository.delete_disciplinas(db, disciplinas_id)
