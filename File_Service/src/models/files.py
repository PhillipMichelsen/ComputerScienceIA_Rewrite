from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    uuid = Column(String, nullable=False)
    bucket_name = Column(String, nullable=False)
    paragraph_count = Column(Integer)
    embedded_paragraph_count = Column(Integer)
    status = Column(String, nullable=False)
