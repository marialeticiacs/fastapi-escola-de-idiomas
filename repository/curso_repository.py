from sqlalchemy.orm import Session
from domain import models, schemas

def get_curso(db: Session, curso_id: int):
    return db.query(models.Curso).filter(models.Curso.id == curso_id).first()

def get_cursos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Curso).offset(skip).limit(limit).all()

def create_curso(db: Session, curso: schemas.CursoCreate):
    db_curso = models.Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def update_curso(db: Session, curso_id: int, curso: schemas.CursoUpdate):
    db_curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if db_curso:
        update_data = curso.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_curso, key, value)
        db.commit()
        db.refresh(db_curso)
    return db_curso

def delete_curso(db: Session, curso_id: int):
    db_curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if db_curso:
        db.delete(db_curso)
        db.commit()
    return db_curso
