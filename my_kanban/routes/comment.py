from flask import Blueprint, abort, flash, redirect, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('comment', __name__, url_prefix='/boards')


@bp.route('/<int:board_id>/cards/<int:card_id>/comments', methods=['POST'])
@jwt_required()
def create(board_id, card_id):
    if not crud.get_card(board_id, card_id):
        abort(404)

    username = get_jwt_identity()

    if not crud.get_user_link_to_board(board_id, username):
        abort(403)

    content = request.form['content']

    if content:
        crud.create_comment(card_id, username, content)
    else:
        flash('Сomment text is required')

    return redirect(url_for("card.handle", board_id=board_id, card_id=card_id), 303)


@bp.route('/<int:board_id>/cards/<int:card_id>/comments/<int:comment_id>', methods=['POST'])
@jwt_required()
def delete(board_id, card_id, comment_id):
    comment = crud.get_comment(comment_id)

    if not comment or comment.card.id != card_id or comment.card.board_id != board_id:
        abort(404)

    username = get_jwt_identity()

    if username != comment.author:
        abort(403)

    if request.form['_method'] == 'DELETE':
        crud.delete_comment(comment)
    else:
        abort(400)

    return redirect(url_for("card.handle", board_id=board_id, card_id=card_id), 303)
