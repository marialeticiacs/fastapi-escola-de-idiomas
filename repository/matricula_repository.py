from sqlalchemy.orm import Session
from domain import models, schemas

def get_matricula(db: Session, matricula_id: int):
    return db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()

def get_matriculas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Matricula).offset(skip).limit(limit).all()

def create_matricula(db: Session, matricula: schemas.MatriculaCreate):
    db_matricula = models.Matricula(**matricula.dict())
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

def update_matricula(db: Session, matricula_id: int, matricula: schemas.MatriculaUpdate):
    db_matricula = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if db_matricula:
        update_data = matricula.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_matricula, key, value)
        db.commit()
        db.refresh(db_matricula)
    return db_matricula

def delete_matricula(db: Session, matricula_id: int):
    db_matricula = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if db_matricula:
        db.delete(db_matricula)
        db.commit()
    return db_matricula
