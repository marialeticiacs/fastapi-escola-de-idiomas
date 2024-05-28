from sqlalchemy.orm import Session
from domain import models, schemas

def get_nivel(db: Session, nivel_id: int):
    return db.query(models.Nivel).filter(models.Nivel.id == nivel_id).first()

def get_niveis(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Nivel).offset(skip).limit(limit).all()

def create_nivel(db: Session, nivel: schemas.NivelCreate):
    db_nivel = models.Nivel(**nivel.dict())
    db.add(db_nivel)
    db.commit()
    db.refresh(db_nivel)
    return db_nivel

def update_nivel(db: Session, db_nivel: models.Nivel):
    db.commit()
    db.refresh(db_nivel)
    return db_nivel

def delete_nivel(db: Session, nivel_id: int):
    db_nivel = db.query(models.Nivel).filter(models.Nivel.id == nivel_id).first()
    db.delete(db_nivel)
    db.commit()
    return db_nivel
