from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List

class ProfessorBase(BaseModel):
    nome: str

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int
    cursos: List['Curso'] = []

    class Config:
        from_attributes = True

class CursoBase(BaseModel):
    nome: str
    data_inicio: date
    data_fim: date

class CursoCreate(CursoBase):
    id_professor: int
    id_sala: int

class Curso(CursoBase):
    id: int
    professor: Professor
    sala: 'Sala'

    class Config:
        from_attributes = True

class AlunoBase(BaseModel):
    nome: str
    dt_nascimento: date

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int
    matriculas: List['Matricula'] = []

    class Config:
        from_attributes = True

class SalaBase(BaseModel):
    insumo: str
    capacidade: int

class SalaCreate(SalaBase):
    pass

class Sala(SalaBase):
    id: int
    cursos: List[Curso] = []

    class Config:
        from_attributes = True

class MatriculaBase(BaseModel):
    data_matricula: date

class MatriculaCreate(MatriculaBase):
    id_aluno: int
    id_curso: int

class Matricula(MatriculaBase):
    id: int
    aluno: Aluno
    curso: Curso

    class Config:
        from_attributes = True
