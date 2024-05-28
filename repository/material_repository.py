from sqlalchemy.orm import Session
from domain import models

def get_material(db: Session, material_id: int):
    return db.query(models.Material).filter(models.Material.id == material_id).first()

def get_materiais(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Material).offset(skip).limit(limit).all()

def create_material(db: Session, material: models.Material):
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

def update_material(db: Session, db_material: models.Material):
    db.commit()
    db.refresh(db_material)
    return db_material

def delete_material(db: Session, material_id: int):
    db_material = get_material(db, material_id)
    db.delete(db_material)
    db.commit()
    return db_material
