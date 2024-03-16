from flask import abort
from sqlalchemy import select

from my_kanban import sqla

from .data.models import Card, user_board


def get_board_info(board_id: int):
    board_info = sqla.session.execute(
        select(user_board).
        where(user_board.c.board_id == board_id)
    ).all()

    if not board_info:
        abort(404)

    return board_info


def get_card(board_id: int, card_id: int) -> Card:
    card = sqla.session.execute(
        select(Card).
        where(Card.board_id == board_id, Card.id == card_id)
    ).scalar_one_or_none()

    if not card:
        abort(404)

    return card
