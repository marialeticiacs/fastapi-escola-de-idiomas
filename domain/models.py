from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    cursos = relationship('Curso', back_populates='professor')

class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    id_professor = Column(Integer, ForeignKey('professores.id'), nullable=False)
    id_sala = Column(Integer, ForeignKey('salas.id'), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)

    professor = relationship('Professor', back_populates='cursos')
    sala = relationship('Sala', back_populates='cursos')
    matriculas = relationship('Matricula', back_populates='curso')

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    dt_nascimento = Column(Date, nullable=False)

    matriculas = relationship('Matricula', back_populates='aluno')

class Sala(Base):
    __tablename__ = 'salas'

    id = Column(Integer, primary_key=True, index=True)
    insumo = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)

    cursos = relationship('Curso', back_populates='sala')

class Matricula(Base):
    __tablename__ = 'matriculas'

    id = Column(Integer, primary_key=True, index=True)
    id_aluno = Column(Integer, ForeignKey('alunos.id'), nullable=False)
    id_curso = Column(Integer, ForeignKey('cursos.id'), nullable=False)
    data_matricula = Column(Date, nullable=False)

    aluno = relationship('Aluno', back_populates='matriculas')
    curso = relationship('Curso', back_populates='matriculas')
