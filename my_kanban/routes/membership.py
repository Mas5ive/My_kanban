from flask import Blueprint, abort, flash, redirect, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from my_kanban import crud

bp = Blueprint('membership', __name__)


@bp.route('/boards/<int:board_id>/invitations', methods=['POST'])
@jwt_required()
def сreate_invitation(board_id):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        abort(400)

    sender = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == sender):
        abort(403)

    recipient = request.form['recipient']

    if not (
        crud.get_user_by_name(recipient)
        and all(link.username != recipient for link in board_links_to_users)
    ):
        abort(400)

    try:
        crud.create_invitation(board_id, recipient, sender)
    except IntegrityError:
        return f'{recipient} has already received an invitation', 409

    flash('the invitation successfully sent!')
    return redirect(url_for("board.handle", board_id=board_id), 303)


@bp.route('/boards/<int:board_id>/users', methods=['POST'])
@jwt_required()
def delete_member(board_id):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        abort(400)

    if not request.form.get('_method') == 'DELETE':
        abort(405)

    username = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == username):
        abort(403)

    other_user = request.form['user']

    if (
        all(link.username != other_user for link in board_links_to_users)
        or other_user == username
    ):
        abort(400)

    crud.delete_member(board_id, other_user)
    return redirect(url_for("board.handle", board_id=board_id), 303)


@bp.route('/profile/invitations', methods=['POST'])
@jwt_required()
def pick_invitation():
    username = get_jwt_identity()
    board_id = request.form['board']
    invitation = crud.get_invitation_by_recipient(board_id, username)

    if not invitation:
        abort(400)

    operation = request.form['operation']

    if operation == 'accept':
        crud.create_member(invitation)
    elif operation == 'reject':
        crud.delete_invitation(invitation)
    else:
        abort(400)

    return redirect(url_for("profile.show"), 303)
