import datetime as dt
from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Domain(Base):
     '''Domain table contains the domains for the indexer'''
     __tablename__='domain'
     id=Column(Integer, primary_key=True, nullable=False)
     name=Column(String(255), nullable=False)
     country=Column(String(3))

     pages = relationship('Page', back_populates='domain')
class Page(Base):
     '''Page table contains the pages to be crawled'''
     __tablename__='page'
     id=Column(Integer, primary_key=True, nullable=False)
     domain_id=Column(Integer, ForeignKey('domain.id'), nullable=False)
     full_url=Column(String(255), nullable=False)
     crawl=Column(Boolean, default=True)
     create_date=Column(DateTime, default=dt.datetime.now())

     domain = relationship('Domain', back_populates='pages')
     responses = relationship('Response', back_populates='page')
class Response(Base):
     '''Response table contains the response of each page when crawled'''
     __tablename__='response'
     id=Column(Integer, primary_key=True, nullable=False)
     page_id=Column(Integer, ForeignKey('page.id'), nullable=False)
     response_code=Column(Integer, nullable=False)
     visit_date=Column(DateTime, default=dt.datetime.now(), nullable=False)
     file_url=Column(String(255))

     page = relationship('Page', back_populates='responses')
