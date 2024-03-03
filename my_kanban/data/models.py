from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from my_kanban import sqla

user_board = Table(
    'user_board',
    sqla.metadata,
    Column('username', ForeignKey('user.name', ondelete='CASCADE'), primary_key=True),
    Column('board_id', ForeignKey('board.id', ondelete='CASCADE'), primary_key=True),
    Column('is_owner', default=0)
)


class User(sqla.Model):
    __tablename__ = 'user'
    name = Column(String, primary_key=True)
    psw_hash = Column(String, nullable=False)

    boards = relationship('Board', secondary=user_board, back_populates='users')


class Board(sqla.Model):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    users = relationship('User', secondary=user_board, back_populates='boards')
    cards = relationship('Card', back_populates='board', cascade='all, delete')


class Invitation(sqla.Model):
    __tablename__ = 'invitation'
    user_recipient = Column(String, ForeignKey('user.name'), primary_key=True)
    board_id = Column(Integer, ForeignKey('board.id', ondelete='CASCADE'), primary_key=True)
    user_sender = Column(String, ForeignKey('user.name'), nullable=False)

    __table_args__ = (
        CheckConstraint("user_sender <> user_recipient"),
    )


class Card(sqla.Model):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True, autoincrement=True)
    board_id = Column(Integer, ForeignKey('board.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String)
    status = Column(Integer, default=0)

    board = relationship('Board', uselist=False)
