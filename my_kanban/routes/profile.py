from collections import defaultdict

from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('profile', __name__)


@bp.route('/profile')
@jwt_required()
def show():
    username = get_jwt_identity()

    boards_info = crud.get_user_boards(username)

    boards = defaultdict(list)
    for board, is_owner in boards_info:
        if is_owner:
            boards['owner boards'].append(board)
        else:
            boards['invitation boards'].append(board)

    invitations = crud.get_recipient_invitations(username)

    return render_template(
        'profile.html',
        username=username,
        owner_boards=boards['owner boards'],
        invitation_boards=boards['invitation boards'],
        invitations=invitations
    )
