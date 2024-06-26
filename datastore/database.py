from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

Base = declarative_base()

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    authors = Column(Text, index=True)
    abstract = Column(Text)
    altmetric_score = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class ErrorScore(Base):
    __tablename__ = 'error_scores'
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('papers.id'), index=True)
    score = Column(Integer)
    explanation = Column(Text)
    scorer = Column(String(255), index=True)
    created_at = Column(DateTime)

# Create database engine and session
engine = create_engine(config('DATABASE_URL', default='sqlite:///mydatabase.db'))
Session = sessionmaker(bind=engine)

# Create tables in the database
Base.metadata.create_all(engine)
