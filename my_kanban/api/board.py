from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('api_board', __name__, url_prefix='/boards')


@bp.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.form
    board_title = data.get('title')

    if not board_title:
        return jsonify({'message': 'The title of the board was not given'}), 400

    username = get_jwt_identity()
    crud.create_board(board_title, username)
    return jsonify({'message': 'Board created successfully'}), 201


@bp.route('/<int:board_id>', methods=['DELETE'])
@jwt_required()
def delete(board_id):
    board = crud.get_board(board_id)

    if not board:
        return jsonify({'message': 'Board not found'}), 404

    username = get_jwt_identity()
    user_link_to_board = crud.get_user_link_to_board(board_id, username)

    if user_link_to_board is None or not user_link_to_board.is_owner:
        return jsonify({'message': 'Access denied'}), 403

    crud.delete_board(board)
    return jsonify({'message': 'Board deleted successfully'}), 200
