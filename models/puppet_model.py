from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

PuppetModel = declarative_base()


class Account(PuppetModel):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column('email', String(255), nullable=False)
    first_name = Column('first_name', String(255), nullable=False)
    last_name = Column('last_name', String(255), nullable=False)
    password = Column('password_hash', String(100), nullable=False)


class Session(PuppetModel):
    __tablename__ = 'session'

    email = Column('email', String(255), nullable=False, primary_key=True)