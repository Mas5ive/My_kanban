from flask import Blueprint, abort, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('card', __name__, url_prefix='/boards/<int:board_id>/cards')


@bp.route('/', methods=['GET'])
@jwt_required()
def create(board_id):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        abort(400)

    username = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == username):
        abort(403)

    return render_template('card/create.html', board_id=board_id)


@bp.route('/<int:card_id>', methods=['GET'])
@jwt_required()
def show(board_id, card_id):
    card = crud.get_card(board_id, card_id)

    if not card:
        abort(404)

    username = get_jwt_identity()
    user_link_to_board = crud.get_user_link_to_board(board_id, username)

    if not user_link_to_board:
        abort(403)

    return render_template(
        'card/view.html',
        card=card,
        board_id=board_id,
        user_info=user_link_to_board
    )
