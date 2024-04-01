from collections import defaultdict

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

    boards_info = sqla.session.execute(
        select(Board, user_board.c.is_owner).
        join(user_board, user_board.c.board_id == Board.id).
        where(user_board.c.username == username)
    ).all()

    boards = defaultdict(list)
    for board, is_owner in boards_info:
        if is_owner:
            boards['owner boards'].append(board)
        else:
            boards['invitation boards'].append(board)

    invitations = sqla.session.execute(
        select(Invitation, Board.title).
        join(Board, Invitation.board_id == Board.id).
        where(Invitation.user_recipient == username)
    ).all()

    return render_template(
        'profile.html',
        username=username,
        owner_boards=boards['owner boards'],
        invitation_boards=boards['invitation boards'],
        invitations=invitations
    )
