from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import aluno_service

router = APIRouter()

@router.get("/alunos/{aluno_id}", response_model=schemas.Aluno)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return aluno_service.get_aluno(db, aluno_id)

@router.get("/alunos/", response_model=List[schemas.Aluno])
def read_alunos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return aluno_service.get_alunos(db, skip, limit)

@router.post("/alunos/", response_model=schemas.Aluno, status_code=status.HTTP_201_CREATED)
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    return aluno_service.create_aluno(db, aluno)


@router.put("/alunos/{aluno_id}", response_model=schemas.Aluno)
def update_aluno(aluno_id: int, aluno: schemas.AlunoUpdate, db: Session = Depends(get_db)):
    return aluno_service.update_aluno(db, aluno_id, aluno)


@router.delete("/alunos/{aluno_id}", response_model=schemas.Aluno)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return aluno_service.delete_aluno(db, aluno_id)
