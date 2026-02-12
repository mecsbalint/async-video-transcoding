from app.database.base import Base
from app.database.session import engine
from app.database import models


def init_db():
    Base.metadata.create_all(bind=engine)
