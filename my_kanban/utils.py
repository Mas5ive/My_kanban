from flask import abort
from sqlalchemy import select

from my_kanban import sqla

from .data.models import user_board


def get_board_info(board_id: int):
    board_info = sqla.session.execute(
        select(user_board).
        where(user_board.c.board_id == board_id)
    ).all()

    if not board_info:
        abort(404)

    return board_info
