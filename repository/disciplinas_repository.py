from sqlalchemy.orm import Session
from domain import models

def get_disciplina(db: Session, disciplinas_id: int):
    return db.query(models.Disciplinas).filter(models.Disciplinas.id == disciplinas_id).first()

def get_disciplinas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Disciplinas).offset(skip).limit(limit).all()

def create_disciplinas(db: Session, disciplinas: models.Disciplinas):
    db.add(disciplinas)
    db.commit()
    db.refresh(disciplinas)
    return disciplinas

def update_disciplinas(db: Session, db_disciplinas: models.Disciplinas):
    db.commit()
    db.refresh(db_disciplinas)
    return db_disciplinas

def delete_disciplinas(db: Session, disciplinas_id: int):
    db_disciplinas = get_disciplina(db, disciplinas_id)
    db.delete(db_disciplinas)
    db.commit()
    return db_disciplinas
