from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository import nivel_repository
from domain import schemas

def get_nivel(db: Session, nivel_id: int):
    nivel = nivel_repository.get_nivel(db, nivel_id)
    if nivel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nivel não encontrado")
    return nivel

def get_niveis(db: Session, skip: int = 0, limit: int = 10):
    return nivel_repository.get_niveis(db, skip, limit)

def create_nivel(db: Session, nivel: schemas.NivelCreate):
    return nivel_repository.create_nivel(db, nivel)

def update_nivel(db: Session, nivel_id: int, nivel: schemas.NivelUpdate): 
    db_nivel = nivel_repository.get_nivel(db, nivel_id)
    if db_nivel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nivel não encontrado")
    
    update_data = nivel.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_nivel, key, value)
    
    return nivel_repository.update_nivel(db, db_nivel)

def delete_nivel(db: Session, nivel_id: int):
    db_nivel = nivel_repository.get_nivel(db, nivel_id)
    if db_nivel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nivel não existe")
    return nivel_repository.delete_nivel(db, nivel_id)
