from flask import Blueprint, abort, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud, utils

bp = Blueprint('board', __name__, url_prefix='/boards')


@bp.route('/<int:board_id>', methods=['GET'])
@jwt_required()
def show(board_id):
    board = crud.get_board(board_id)

    if not board:
        abort(404)

    username = get_jwt_identity()
    user_link_to_board = crud.get_user_link_to_board(board_id, username)

    if not user_link_to_board:
        abort(403)

    return render_template(
        'board.html',
        board=board,
        grouped_cards=utils.get_card_groups(board.cards),
        user_board_info=user_link_to_board
    )
