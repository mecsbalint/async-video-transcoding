from sqlalchemy import Column, Integer, String
from base import Base


class TestTable(Base):
    __tablename__ = "testtable"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
