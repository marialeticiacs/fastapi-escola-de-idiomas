from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import sala_service

router = APIRouter()

@router.get("/salas/{sala_id}", response_model=schemas.Sala)
def read_sala(sala_id: int, db: Session = Depends(get_db)):
    return sala_service.get_sala(db, sala_id)

@router.get("/salas/", response_model=List[schemas.Sala])
def read_salas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return sala_service.get_salas(db, skip, limit)

@router.post("/salas/", response_model=schemas.Sala, status_code=status.HTTP_201_CREATED)
def create_sala(sala: schemas.SalaCreate, db: Session = Depends(get_db)):
    return sala_service.create_sala(db, sala)

@router.put("/salas/{sala_id}", response_model=schemas.Sala)
def update_sala(sala_id: int, sala: schemas.SalaUpdate, db: Session = Depends(get_db)):
    return sala_service.update_sala(db, sala_id, sala)

@router.delete("/salas/{sala_id}", response_model=schemas.Sala)
def delete_sala(sala_id: int, db: Session = Depends(get_db)):
    return sala_service.delete_sala(db, sala_id)
