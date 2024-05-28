from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from domain import schemas
from service import material_service

router = APIRouter()

@router.get("/materiais/{material_id}", response_model=schemas.Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    return material_service.get_material(db, material_id)

@router.get("/materiais/", response_model=List[schemas.Material])
def read_materiais(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return material_service.get_materiais(db, skip, limit)

@router.post("/materiais/", response_model=schemas.Material, status_code=status.HTTP_201_CREATED)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return material_service.create_material(db, material)

@router.put("/materiais/{material_id}", response_model=schemas.Material)
def update_material(material_id: int, material: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    return material_service.update_material(db, material_id, material)

@router.delete("/materiais/{material_id}", response_model=schemas.Material)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    return material_service.delete_material(db, material_id)