from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository import aluno_repository
from domain import schemas

def get_aluno(db: Session, aluno_id: int):
    aluno = aluno_repository.get_aluno(db, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    return aluno

def get_alunos(db: Session, skip: int = 0, limit: int = 10):
    return aluno_repository.get_alunos(db, skip, limit)

def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    return aluno_repository.create_aluno(db, aluno)

def update_aluno(db: Session, aluno_id: int, aluno: schemas.AlunoUpdate):
    db_aluno = aluno_repository.get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    
    update_data = aluno.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_aluno, key, value)
    
    return aluno_repository.update_aluno(db, db_aluno)

def delete_aluno(db: Session, aluno_id: int):
    db_aluno = aluno_repository.get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não existe")
    return aluno_repository.delete_aluno(db, aluno_id)
