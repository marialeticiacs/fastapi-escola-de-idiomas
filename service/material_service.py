from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository import material_repository
from domain import schemas, models

def get_material(db: Session, material_id: int):
    material = material_repository.get_material(db, material_id)
    if material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")
    return material

def get_materiais(db: Session, skip: int = 0, limit: int = 10):
    return material_repository.get_materiais(db, skip, limit)

def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(**material.model_dump())
    return material_repository.create_material(db, db_material)

def update_material(db: Session, material_id: int, material: schemas.MaterialUpdate):
    db_material = material_repository.get_material(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")
    
    update_data = material.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_material, key, value)
    
    return material_repository.update_material(db, db_material)

def delete_material(db: Session, material_id: int):
    db_material = material_repository.get_material(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")
    return material_repository.delete_material(db, material_id)
