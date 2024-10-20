from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

USUARIO = 'root'
HOST = 'localhost'
PORT = 3306
PWD = 1103
BANCO = 'logincli'

con = f'mysql+pymysql://{USUARIO}:{PWD}@{HOST}:{PORT}/{BANCO}'