from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository import sala_repository
from domain import schemas, models

def get_sala(db: Session, sala_id: int):
    sala = sala_repository.get_sala(db, sala_id)
    if sala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    return sala

def get_salas(db: Session, skip: int = 0, limit: int = 10):
    return sala_repository.get_salas(db, skip, limit)

def create_sala(db: Session, sala: schemas.SalaCreate):
    db_sala = models.Sala(**sala.model_dump())
    return sala_repository.create_sala(db, db_sala)

def update_sala(db: Session, sala_id: int, sala: schemas.SalaUpdate):
    db_sala = sala_repository.get_sala(db, sala_id)
    if db_sala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    
    update_data = sala.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sala, key, value)
    
    return sala_repository.update_sala(db, db_sala)

def delete_sala(db: Session, sala_id: int):
    db_sala = sala_repository.get_sala(db, sala_id)
    if db_sala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="essa sala não existe")
    return sala_repository.delete_sala(db, sala_id)
