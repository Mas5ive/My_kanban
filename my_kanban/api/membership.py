from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from my_kanban import crud

bp = Blueprint('api_membership', __name__)


@bp.route('/boards/<int:board_id>/invitations', methods=['POST'])
@jwt_required()
def create_invitation(board_id):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        return jsonify({'message': 'Board not found'}), 404

    sender = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == sender):
        return jsonify({'message': 'Access denied'}), 403

    data = request.form
    recipient = data.get('recipient')

    if not (
        crud.get_user_by_name(recipient)
        and all(link.username != recipient for link in board_links_to_users)
    ):
        return jsonify({'message': 'User not found or is already a member'}), 400

    try:
        crud.create_invitation(board_id, recipient, sender)
    except IntegrityError:
        return jsonify({'message': f'{recipient} has already received an invitation'}), 409

    return jsonify({'message': 'Invitation sent successfully'}), 201


@bp.route('/boards/<int:board_id>/users/<string:other_user>', methods=['DELETE'])
@jwt_required()
def delete_member(board_id, other_user):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        return jsonify({'message': 'Board not found'}), 404

    username = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == username):
        return jsonify({'message': 'Access denied'}), 403

    if (
        all(link.username != other_user for link in board_links_to_users)
        or other_user == username
    ):
        return jsonify({'message': 'User not found or is the owner'}, 400)

    crud.delete_member(board_id, other_user)
    return jsonify({'message': f'The {other_user} has been successfully deleted'}), 200


@bp.route('/profile/invitations', methods=['POST'])
@jwt_required()
def pick_invitation():
    username = get_jwt_identity()
    data = request.form
    board_id = data.get('board')
    operation = data.get('operation')

    if not board_id or not operation:
        return jsonify({'message': 'The board and operation parameters are required'}), 400

    invitation = crud.get_invitation_by_recipient(board_id, username)

    if not invitation:
        return jsonify({'message': 'Invitation not found or already processed'}), 404

    if operation == 'accept':
        crud.create_member(invitation)
        return jsonify({'message': 'The invitation has been accepted'}), 201
    elif operation == 'reject':
        crud.delete_invitation(invitation)
        return jsonify({'message': 'The invitation has been rejected'}), 200
    else:
        return jsonify({'message': 'Invalid operation specified'}), 400
