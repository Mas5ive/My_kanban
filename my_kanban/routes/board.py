from collections import defaultdict
from typing import Any

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('board', __name__)


def get_card_groups(cards: list) -> defaultdict[Any, list]:
    grouped_cards = defaultdict(list)
    for card in cards:
        grouped_cards[card.status].append(card)
    return grouped_cards


@bp.route('/boards/<int:board_id>', methods=['GET', 'POST'])
@jwt_required()
def handle(board_id):
    board = crud.get_board(board_id)

    if board is None:
        abort(404)

    board_links_to_users = crud.get_board_links_to_users(board_id)
    username = get_jwt_identity()
    user_board_info = next((link for link in board_links_to_users if link.username == username), None)

    if user_board_info is None:
        abort(403)

    if request.method == 'POST':
        if user_board_info.is_owner and request.form.get('_method') == 'DELETE':
            crud.delete_board(board)
            return redirect(url_for("profile.show"), 303)
        else:
            abort(403)

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
        username = get_jwt_identity()
        crud.create_board(board_title, username)
        return redirect(url_for("profile.show"), 303)
