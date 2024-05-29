from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    cpf = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    cursos = relationship('Curso', back_populates='professor')

class Curso(Base):
    __tablename__ = "cursos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    id_professor = Column(Integer, ForeignKey("professores.id"))
    id_nivel = Column(Integer, ForeignKey("niveis.id"))
    id_material = Column(Integer, ForeignKey("materiais.id"))
    id_sala = Column(Integer, ForeignKey("salas.id"))
    descricao = Column(String)
    data_inicio = Column(Date)
    data_fim = Column(Date)
    
    professor = relationship("Professor", back_populates="cursos")
    nivel = relationship("Nivel", back_populates="cursos")
    material = relationship("Material", back_populates="cursos")
    sala = relationship("Sala", back_populates="cursos")
    matriculas = relationship("Matricula", back_populates="curso")

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    dt_nascimento = Column(Date, nullable=False)

    matriculas = relationship('Matricula', back_populates='aluno')

class Sala(Base):
    __tablename__ = 'salas'

    id = Column(Integer, primary_key=True, index=True)
    insumo = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)
    cursos = relationship('Curso', back_populates='sala')

class Matricula(Base):
    __tablename__ = "matriculas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id"))
    id_curso = Column(Integer, ForeignKey("cursos.id"))
    data_matricula = Column(Date)
    
    aluno = relationship("Aluno", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculas")

class Nivel(Base):
    __tablename__ = 'niveis'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    descricao = Column(String, nullable=True)
    cursos = relationship('Curso', back_populates='nivel')

class Material(Base):
    __tablename__ = 'materiais'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    cursos = relationship('Curso', back_populates='material')
