from sqlalchemy.orm import Session
from domain import models

def get_sala(db: Session, sala_id: int):
    return db.query(models.Sala).filter(models.Sala.id == sala_id).first()

def get_salas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Sala).offset(skip).limit(limit).all()

def create_sala(db: Session, sala: models.Sala):
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala

def update_sala(db: Session, db_sala: models.Sala):
    db.commit()
    db.refresh(db_sala)
    return db_sala

def delete_sala(db: Session, sala_id: int):
    db_sala = get_sala(db, sala_id)
    db.delete(db_sala)
    db.commit()
    return db_sala
