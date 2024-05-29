from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service import matricula_service
from domain import schemas
from app.database import get_db

router = APIRouter()

@router.get("/matriculas/{matricula_id}", response_model=schemas.Matricula)
def read_matricula(matricula_id: int, db: Session = Depends(get_db)):
    db_matricula = matricula_service.get_matricula(db, matricula_id)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matricula not found")
    return db_matricula

@router.get("/matriculas/", response_model=list[schemas.Matricula])
def read_matriculas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    matriculas = matricula_service.get_matriculas(db, skip=skip, limit=limit)
    return matriculas

@router.post("/matriculas/", response_model=schemas.Matricula)
def create_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    return matricula_service.create_matricula(db, matricula)

@router.put("/matriculas/{matricula_id}", response_model=schemas.Matricula)
def update_matricula(matricula_id: int, matricula: schemas.MatriculaUpdate, db: Session = Depends(get_db)):
    db_matricula = matricula_service.get_matricula(db, matricula_id)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matricula not found")
    return matricula_service.update_matricula(db, matricula_id, matricula)

@router.delete("/matriculas/{matricula_id}", response_model=schemas.Matricula)
def delete_matricula(matricula_id: int, db: Session = Depends(get_db)):
    db_matricula = matricula_service.get_matricula(db, matricula_id)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matricula not found")
    return matricula_service.delete_matricula(db, matricula_id)