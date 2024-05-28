from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import nivel_service

router = APIRouter()

@router.get("/niveis/{nivel_id}", response_model=schemas.Nivel)
def read_nivel(nivel_id: int, db: Session = Depends(get_db)):
    return nivel_service.get_nivel(db, nivel_id)

@router.get("/niveis/", response_model=List[schemas.Nivel])
def read_niveis(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return nivel_service.get_niveis(db, skip, limit)

@router.post("/niveis/", response_model=schemas.Nivel, status_code=status.HTTP_201_CREATED)
def create_nivel(nivel: schemas.NivelCreate, db: Session = Depends(get_db)):
    return nivel_service.create_nivel(db, nivel)

@router.put("/niveis/{nivel_id}", response_model=schemas.Nivel)
def update_nivel(nivel_id: int, nivel: schemas.NivelUpdate, db: Session = Depends(get_db)):  
    return nivel_service.update_nivel(db, nivel_id, nivel)

@router.delete("/niveis/{nivel_id}", response_model=schemas.Nivel)
def delete_nivel(nivel_id: int, db: Session = Depends(get_db)):
    return nivel_service.delete_nivel(db, nivel_id)
