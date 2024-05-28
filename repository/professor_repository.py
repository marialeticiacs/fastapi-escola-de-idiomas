from sqlalchemy.orm import Session
from domain import models, schemas

def get_professor(db: Session, professor_id: int):
    return db.query(models.Professor).filter(models.Professor.id == professor_id).first()

def get_professors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Professor).offset(skip).limit(limit).all()

def create_professor(db: Session, professor: schemas.ProfessorCreate):
    db_professor = models.Professor(**professor.dict())
    db_professor = models.Professor(nome=professor.nome)
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def update_professor(db: Session, db_professor: models.Professor):
    db.commit()
    db.refresh(db_professor)
    return db_professor

def delete_professor(db: Session, professor_id: int):
    db_professor = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    db.delete(db_professor)
    db.commit()
    return db_professor

