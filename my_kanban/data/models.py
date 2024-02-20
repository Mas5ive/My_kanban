from my_kanban import sqla
from sqlalchemy import Column, String


class User(sqla.Model):
    __tablename__ = 'user'
    name = Column(String, primary_key=True)
    psw_hash = Column(String, nullable=False)
