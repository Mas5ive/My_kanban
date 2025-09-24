from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('api_card', __name__, url_prefix='/boards/<int:board_id>/cards')


@bp.route('/', methods=['POST'])
@jwt_required()
def create(board_id):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        return jsonify({'message': 'Board not found'}), 404

    username = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == username):
        return jsonify({'message': 'Access denied'}), 403

    data = request.form
    title = data.get('title')

    if not title:
        return jsonify({'message': 'The title of the card was not given'}), 400

    content = data.get('content')
    crud.create_card(board_id, title, content)
    return jsonify({'message': 'Card created successfully'}), 201


@bp.route('/<int:card_id>', methods=['POST'])
@jwt_required()
def change(board_id, card_id):
    username = get_jwt_identity()
    user_link_to_board = crud.get_user_link_to_board(board_id, username)

    if not user_link_to_board:
        return jsonify({'message': 'Access denied'}), 403

    card = crud.get_card(board_id, card_id)

    if not card:
        return jsonify({'message': 'Card not found'}), 404

    data = request.form
    operation = data.get('operation')

    if operation in ('MOVE_LEFT', 'MOVE_RIGHT'):
        try:
            crud.move_card(card, operation)
        except ValueError as e:
            return jsonify({'message': str(e)}), 400

        return jsonify({'message': 'Card moved successfully'}), 200

    elif operation == 'EDIT':
        if not user_link_to_board.is_owner:
            return jsonify({'message': 'Access denied'}), 403

        title = data.get('title')
        content = data.get('content')

        if not title:
            crud.edit_card(card, content=content)
            return jsonify({'message': 'Saved, but the title can not be empty'}), 200
        else:
            crud.edit_card(card, title=title, content=content)
            return jsonify({'message': 'Saved'}), 200
    else:
        return jsonify({'message': 'Invalid operation'}), 400


@bp.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
def delete(board_id, card_id):
    username = get_jwt_identity()
    user_link_to_board = crud.get_user_link_to_board(board_id, username)

    if not (user_link_to_board and user_link_to_board.is_owner):
        return jsonify({'message': 'Access denied'}), 403

    card = crud.get_card(board_id, card_id)

    if not card:
        return jsonify({'message': 'Card not found'}), 404

    crud.delete_card(card)
    return jsonify({'message': 'Card deleted successfully'}), 200
