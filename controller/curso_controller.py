from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service import curso_service 
from domain import schemas
from app.database import get_db

router = APIRouter()

@router.get("/cursos/{curso_id}", response_model=schemas.Curso)
def read_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = curso_service.get_curso(db, curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso not found")
    return db_curso

@router.get("/cursos/", response_model=list[schemas.Curso])
def read_cursos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cursos = curso_service.get_cursos(db, skip=skip, limit=limit)
    return cursos

@router.post("/cursos/", response_model=schemas.Curso)
def create_curso(curso: schemas.CursoCreate, db: Session = Depends(get_db)):
    return curso_service.create_curso(db, curso)

@router.put("/cursos/{curso_id}", response_model=schemas.Curso)
def update_curso(curso_id: int, curso: schemas.CursoUpdate, db: Session = Depends(get_db)):
    db_curso = curso_service.get_curso(db, curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso not found")
    return curso_service.update_curso(db, curso_id, curso)

@router.delete("/cursos/{curso_id}", response_model=schemas.Curso)
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = curso_service.get_curso(db, curso_id)
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso not found")
    return curso_service.delete_curso(db, curso_id)
