from flask import Blueprint, abort, flash, redirect, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select

from my_kanban import sqla

from .data.models import Comment, user_board
from .utils import get_card

bp = Blueprint('comment', __name__, url_prefix='/boards')


@bp.route('/<int:board_id>/cards/<int:card_id>/comments', methods=['POST'])
@jwt_required()
def create(board_id, card_id):
    get_card(board_id, card_id)
    username = get_jwt_identity()

    if not (
        sqla.session.query(
            select(user_board).
            where(user_board.c.board_id == board_id, user_board.c.username == username).
            exists()
        ).scalar()
    ):
        abort(403)

    content = request.form['content']
    if content:
        new_comment = Comment(card_id=card_id, author=username, content=content)
        sqla.session.add(new_comment)
        sqla.session.commit()
    else:
        flash('Сomment text is required')

    return redirect(url_for("card.handle", board_id=board_id, card_id=card_id), 303)


@bp.route('/<int:board_id>/cards/<int:card_id>/comments/<int:comment_id>', methods=['POST'])
@jwt_required()
def delete(board_id, card_id, comment_id):
    comment = sqla.session.execute(
        select(Comment).
        where(Comment.id == comment_id)
    ).scalar_one_or_none()

    if not comment or comment.card.id != card_id or comment.card.board_id != board_id:
        abort(404)

    username = get_jwt_identity()
    if username != comment.author:
        abort(403)

    if request.form['_method'] == 'DELETE':
        sqla.session.delete(comment)
        sqla.session.commit()
    else:
        abort(400)

    return redirect(url_for("card.handle", board_id=board_id, card_id=card_id), 303)
