from sqlalchemy import Column, Integer, String
from app.database.base import Base


class TestTable(Base):
    __tablename__ = "testtabletwo"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
