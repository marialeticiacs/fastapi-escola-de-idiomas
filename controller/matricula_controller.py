from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import matricula_service

router = APIRouter()

@router.get("/matriculas/{matricula_id}", response_model=schemas.Matricula)
def read_matricula(matricula_id: int, db: Session = Depends(get_db)):
    db_matricula = matricula_service.get_matricula(db, matricula_id)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return db_matricula

@router.get("/matriculas/", response_model=List[schemas.Matricula])
def read_matriculas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    matriculas = matricula_service.get_matriculas(db, skip=skip, limit=limit)
    return matriculas

@router.post("/matriculas/", response_model=schemas.Matricula, status_code=status.HTTP_201_CREATED)
def create_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    return matricula_service.create_matricula(db, matricula)

@router.put("/matriculas/{matricula_id}", response_model=schemas.Matricula)
def update_matricula(matricula_id: int, matricula: schemas.MatriculaUpdate, db: Session = Depends(get_db)):
    db_matricula = matricula_service.get_matricula(db, matricula_id)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return matricula_service.update_matricula(db, matricula_id, matricula)

@router.delete("/matriculas/{matricula_id}", response_model=schemas.Matricula)
def delete_matricula(matricula_id: int, db: Session = Depends(get_db)):
    db_matricula = matricula_service.get_matricula(db, matricula_id)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return matricula_service.delete_matricula(db, matricula_id)
