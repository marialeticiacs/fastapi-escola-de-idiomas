from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import professor_service

router = APIRouter()

@router.get("/professores/{professor_id}", response_model=schemas.Professor)
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    return professor_service.get_professor(db, professor_id)

@router.get("/professores/", response_model=List[schemas.Professor])
def read_professors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return professor_service.get_professors(db, skip, limit)

@router.post("/professores/", response_model=schemas.Professor, status_code=status.HTTP_201_CREATED)
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    return professor_service.create_professor(db, professor)

@router.put("/professores/{professor_id}", response_model=schemas.Professor)
def update_professor(professor_id: int, professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    return professor_service.update_professor(db, professor_id, professor)

@router.delete("/professores/{professor_id}", response_model=schemas.Professor)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    return professor_service.delete_professor(db, professor_id)
