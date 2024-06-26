from collections import defaultdict
from typing import Any

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from my_kanban import sqla

from .data.models import Board, user_board
from .utils import get_board_info

bp = Blueprint('board', __name__)


def get_board(board_id: int) -> Board:
    return sqla.session.execute(
        select(Board).
        options(joinedload(Board.users), selectinload(Board.cards)).
        where(Board.id == board_id)
    ).unique().scalar_one()


def get_card_groups(cards: list) -> defaultdict[Any, list]:
    grouped_cards = defaultdict(list)
    for card in cards:
        grouped_cards[card.status].append(card)
    return grouped_cards


@bp.route('/boards/<int:board_id>', methods=['GET', 'POST'])
@jwt_required()
def handle(board_id):
    board_info = get_board_info(board_id)
    username = get_jwt_identity()
    user_board_info = next((info for info in board_info if info.username == username), None)

    if user_board_info is None:
        abort(403)

    if request.method == 'POST':
        if user_board_info.is_owner and request.form.get('_method') == 'DELETE':
            sqla.session.delete(get_board(board_id))
            sqla.session.commit()
            return redirect(url_for("profile.show"), 303)
        else:
            abort(403)

    board = get_board(board_id)

    return render_template(
        'board.html',
        board=board,
        grouped_cards=get_card_groups(board.cards),
        user_board_info=user_board_info
    )


@bp.route('/boards', methods=['POST'])
@jwt_required()
def create():
    board_title = request.form['title']

    if not board_title:
        return 'The title of the board was not given', 400
    else:
        with sqla.session.begin_nested():
            new_board = Board(title=board_title)
            sqla.session.add(new_board)
            sqla.session.flush()

            username = get_jwt_identity()
            sqla.session.execute(
                user_board.insert().
                values(username=username, board_id=new_board.id, is_owner=1)
            )
        sqla.session.commit()
        return redirect(url_for("profile.show"), 303)
