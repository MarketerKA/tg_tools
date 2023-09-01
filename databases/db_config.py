from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ALCHEMY_URL = "sqlite:///spammed_users.db"

engine = create_engine(ALCHEMY_URL)

SessonLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    with SessonLocal() as session:
        yield session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, index=True)
    spammed = Column(Boolean, index=True)
