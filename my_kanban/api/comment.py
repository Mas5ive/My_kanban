from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('api_comment', __name__, url_prefix='/boards/<int:board_id>/cards/<int:card_id>/comments')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_comments(board_id, card_id):
    card = crud.get_card(board_id, card_id)

    if not card:
        return jsonify({'message': 'Card not found'}), 404

    username = get_jwt_identity()

    if not crud.get_user_link_to_board(board_id, username):
        return jsonify({'message': 'Access denied'}), 403

    comments = [
        {'id': comments.id, 'author': comments.author, 'content': comments.content, 'date': comments.date.isoformat()}
        for comments in card.comments
    ]

    return jsonify(comments), 200


@bp.route('/', methods=['POST'])
@jwt_required()
def create(board_id, card_id):
    if not crud.get_card(board_id, card_id):
        return jsonify({'message': 'Card not found'}), 404

    username = get_jwt_identity()

    if not crud.get_user_link_to_board(board_id, username):
        return jsonify({'message': 'Access denied'}), 403

    data = request.form
    content = data.get('content')

    if not content:
        return jsonify({'message': 'The comment text was not given'}), 400

    crud.create_comment(card_id, username, content)
    return jsonify({'message': 'Comment created successfully'}), 201


@bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete(board_id, card_id, comment_id):
    comment = crud.get_comment(comment_id)

    if not comment or comment.card.id != card_id or comment.card.board_id != board_id:
        return jsonify({'message': 'Comment not found'}), 404

    username = get_jwt_identity()

    if username != comment.author:
        return jsonify({'message': 'Access denied'}), 403

    crud.delete_comment(comment)
    return jsonify({'message': 'Comment deleted successfully'}), 200
