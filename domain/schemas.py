from typing import Optional, List
from pydantic import BaseModel
from datetime import date

class ProfessorBase(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int

    class Config:
        orm_mode = True

class CursoBase(BaseModel):
    nome: str
    id_professor: int
    id_nivel: int
    id_disciplinas: int
    id_sala: int
    descricao: Optional[str] = None
    data_inicio: date
    data_fim: date

class CursoCreate(CursoBase):
    pass

class Curso(CursoBase):
    id: int
    professor: Optional[Professor] = None
    nivel: Optional['Nivel'] = None
    disciplinas: Optional['Disciplinas'] = None
    sala: Optional['Sala'] = None

    class Config:
        orm_mode = True

class CursoUpdate(BaseModel):
    nome: Optional[str] = None
    id_professor: Optional[int] = None
    id_nivel: Optional[int] = None
    id_disciplinas: Optional[int] = None
    id_sala: Optional[int] = None
    descricao: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None

    class Config:
        orm_mode = True

class AlunoBase(BaseModel):
    nome: str
    cpf: str
    email: str
    dt_nascimento: date

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    dt_nascimento: Optional[date] = None

class Aluno(AlunoBase):
    id: int

    class Config:
        orm_mode = True

class SalaBase(BaseModel):
    nome: str
    capacidade: int

class SalaCreate(SalaBase):
    pass

class SalaUpdate(BaseModel):
    nome: Optional[str] = None
    capacidade: Optional[int] = None

class Sala(SalaBase):
    id: int

    class Config:
        orm_mode = True

class MatriculaBase(BaseModel):
    id_aluno: int
    id_curso: int
    data_matricula: date

class MatriculaCreate(MatriculaBase):
    pass

class Matricula(MatriculaBase):
    id: int

    class Config:
        orm_mode = True

class MatriculaUpdate(BaseModel):
    id_aluno: Optional[int] = None
    id_curso: Optional[int] = None
    data_matricula: Optional[date] = None

    class Config:
        orm_mode = True

class NivelBase(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class NivelCreate(NivelBase):
    pass

class NivelUpdate(NivelBase):
    pass

class Nivel(NivelBase):
    id: int

    class Config:
        orm_mode = True

class DisciplinasBase(BaseModel):
    nome: str
    descricao: str

class DisciplinasCreate(DisciplinasBase):
    pass

class DisciplinasUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class Disciplinas(DisciplinasBase):
    id: int

    class Config:
        orm_mode = True
