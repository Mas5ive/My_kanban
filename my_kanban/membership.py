from flask import Blueprint, abort, flash, redirect, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from my_kanban import sqla

from .data.models import Invitation, User, user_board
from .utils import get_board_info

bp = Blueprint('membership', __name__)


@bp.route('/boards/<int:board_id>/invitations', methods=['POST'])
@jwt_required()
def сreate_invitation(board_id):
    board_info = get_board_info(board_id)
    sender = get_jwt_identity()

    if not any(info.is_owner for info in board_info if info.username == sender):
        abort(403)

    recipient = request.form['recipient']
    if not (
        sqla.session.query(
            select(User).
            where(User.name == recipient).exists()
        ).scalar()
        and all(info.username != recipient for info in board_info)
    ):
        abort(400)

    invitation = Invitation(
        user_recipient=recipient,
        board_id=board_id,
        user_sender=sender
    )
    try:
        sqla.session.add(invitation)
        sqla.session.commit()
    except IntegrityError:
        return f'{recipient} has already received an invitation', 409

    flash('the invitation successfully sent!')
    return redirect(url_for("board.handle", board_id=board_id), 303)


@bp.route('/boards/<int:board_id>/users', methods=['POST'])
@jwt_required()
def delete_member(board_id):
    if not request.form.get('_method') == 'DELETE':
        abort(405)

    board_info = get_board_info(board_id)
    username = get_jwt_identity()

    if not any(info.is_owner for info in board_info if info.username == username):
        abort(403)

    other_user = request.form['user']

    if (
        all(info.username != other_user for info in board_info)
        or other_user == username
    ):
        abort(400)

    sqla.session.execute(
        user_board.delete().
        where(user_board.c.username == other_user, user_board.c.board_id == board_id)
    )
    sqla.session.commit()

    return redirect(url_for("board.handle", board_id=board_id), 303)


@bp.route('/profile/invitations', methods=['POST'])
@jwt_required()
def pick_invitation():
    username = get_jwt_identity()
    board_id = request.form['board']

    invitation = sqla.session.execute(
        select(Invitation).
        where(Invitation.board_id == board_id, Invitation.user_recipient == username)
    ).scalar_one_or_none()

    if not invitation:
        abort(400)

    operation = request.form['operation']
    if operation == 'accept':
        with sqla.session.begin_nested():
            sqla.session.delete(invitation)
            sqla.session.execute(
                user_board.insert().values(username=username, board_id=board_id)
            )
    elif operation == 'reject':
        sqla.session.delete(invitation)
    else:
        abort(400)

    sqla.session.commit()
    return redirect(url_for("profile.show"), 303)
