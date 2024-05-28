from typing import Optional, List
from pydantic import BaseModel, ConfigDict
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
    cursos: List['Curso'] = []

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)

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
    matriculas: List['Matricula'] = []

    model_config = ConfigDict(from_attributes=True)

class SalaBase(BaseModel):
    insumo: str
    capacidade: int

class SalaCreate(SalaBase):
    pass

class Sala(SalaBase):
    id: int
    cursos: List[Curso] = []

    model_config = ConfigDict(from_attributes=True)

class MatriculaBase(BaseModel):
    data_matricula: date

class MatriculaCreate(MatriculaBase):
    id_aluno: int
    id_curso: int

class Matricula(MatriculaBase):
    id: int
    aluno: Aluno
    curso: Curso

    model_config = ConfigDict(from_attributes=True)

class NivelBase(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class NivelCreate(NivelBase):
    pass

class NivelUpdate(NivelBase):
    pass

class Nivel(NivelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
