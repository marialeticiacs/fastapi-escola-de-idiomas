from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import disciplinas_service

router = APIRouter()

@router.get("/disciplinas/{disciplinas_id}", response_model=schemas.Disciplinas)
def read_disciplinas(disciplinas_id: int, db: Session = Depends(get_db)):
    return disciplinas_service.get_disciplina(db, disciplinas_id)

@router.get("/disciplinas/", response_model=List[schemas.Disciplinas])
def read_disciplinas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return disciplinas_service.get_disciplinas(db, skip, limit)

@router.post("/disciplinas/", response_model=schemas.Disciplinas, status_code=status.HTTP_201_CREATED)
def create_disciplinas(disciplinas: schemas.DisciplinasCreate, db: Session = Depends(get_db)):
    return disciplinas_service.create_disciplinas(db, disciplinas)

@router.put("/disciplinas/{disciplinas_id}", response_model=schemas.Disciplinas)
def update_disciplinas(disciplinas_id: int, disciplinas: schemas.DisciplinasUpdate, db: Session = Depends(get_db)):
    return disciplinas_service.update_disciplinas(db, disciplinas_id, disciplinas)

@router.delete("/disciplinas/{disciplinas_id}", response_model=schemas.Disciplinas)
def delete_disciplinas(disciplinas_id: int, db: Session = Depends(get_db)):
    return disciplinas_service.delete_disciplinas(db, disciplinas_id)