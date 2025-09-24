from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud, utils

bp = Blueprint('api_profile', __name__, url_prefix='/profile')


@bp.route('/boards', methods=['GET'])
@jwt_required()
def get_boards():
    username = get_jwt_identity()
    boards_info = crud.get_user_boards(username)
    boards = utils.split_boards(boards_info)
    return jsonify({
        'owner_boards': [{'id': b.id, 'title': b.title} for b in boards['owner boards']],
        'member_boards': [{'id': b.id, 'title': b.title} for b in boards['member boards']]
    }), 200


@bp.route('/invitations', methods=['GET'])
@jwt_required()
def get_invitations():
    username = get_jwt_identity()
    invitations = crud.get_recipient_invitations(username)
    data = [
        {
            'board_id': inv.board_id,
            'board_title': board_title,
            'sender': inv.user_sender
        }
        for inv, board_title in invitations
    ]
    return jsonify(data), 200
