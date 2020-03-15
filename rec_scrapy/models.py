import datetime as dt
from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Domain(Base):
     '''Domain table contains the domains for the indexer'''
     __tablename__='domain'
     id=Column(Integer, primary_key=True)
     name=Column(String(255))
     country=Column(String(3))

     pages = relationship('Page', back_populates='domain')
class Page(Base):
     '''Page table contains the pages to be crawled'''
     __tablename__='page'
     id=Column(Integer, primary_key=True)
     domain_id=Column(Integer, ForeignKey('domain.id'))
     full_url=Column(String(255))
     crawl=Column(Boolean, default=True)

     domain = relationship('Domain', back_populates='pages')
     responses = relationship('Response', back_populates='page')
class Response(Base):
     '''Response table contains the response of each page when crawled'''
     __tablename__='response'
     id=Column(Integer, primary_key=True)
     page_id=Column(Integer, ForeignKey('page.id'))
     response_code=Column(Integer)
     visit_date=Column(DateTime, default=dt.datetime.now())
     file_url=Column(String(255))

     page = relationship('Page', back_populates='responses')
