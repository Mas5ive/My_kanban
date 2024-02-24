from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select

from my_kanban import sqla

from .data.models import Board, Invitation, user_board

bp = Blueprint('profile', __name__)


@bp.route('/profile')
@jwt_required()
def show():
    username = get_jwt_identity()

    owner_boards = sqla.session.execute(
        select(Board).
        join(user_board, user_board.c.board_id == Board.id).
        where(user_board.c.username == username, user_board.c.is_owner == 1)
    ).scalars().all()

    invitation_boards = sqla.session.execute(
        select(Board).
        join(user_board, user_board.c.board_id == Board.id).
        where(user_board.c.username == username, user_board.c.is_owner == 0)
    ).scalars().all()

    invitations = sqla.session.execute(
        select(Invitation, Board.title).
        join(Board, Invitation.board_id == Board.id).
        where(Invitation.user_recipient == username)
    ).all()

    return render_template(
        'profile.html',
        username=username,
        owner_boards=owner_boards,
        invitation_boards=invitation_boards,
        invitations=invitations
    )
