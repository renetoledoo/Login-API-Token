from venv import create

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from pydantic import BaseModel

USUARIO = 'root'
HOST = 'localhost'
PORT = 3306
PWD = 1103
BANCO = 'logincli'

con = f'mysql+pymysql://{USUARIO}:{PWD}@{HOST}:{PORT}/{BANCO}'

engine = create_engine(con)
Session = sessionmaker(bind=engine)
session_min = Session()
Base = declarative_base()


class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50))
    usuario = Column(String(20))
    senha = Column(String(10))


class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('Pessoa.id'))
    token = Column(String(32))
    data = Column(DateTime, default=datetime.now())
    data_expiracao = Column(DateTime)

class PessoaModelo(BaseModel):
    nome: str
    usuario: str
    senha: str

class LoginModelo(BaseModel):
    usuario: str
    senha: str
Base.metadata.create_all(engine)
