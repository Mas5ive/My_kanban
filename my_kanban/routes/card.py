from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_jwt_extended import get_jwt_identity, jwt_required

from my_kanban import crud

bp = Blueprint('card', __name__, url_prefix='/boards')


@bp.route('/<int:board_id>/cards', methods=['GET', 'POST'])
@jwt_required()
def create(board_id):
    board_links_to_users = crud.get_board_links_to_users(board_id)

    if not board_links_to_users:
        abort(400)

    username = get_jwt_identity()

    if not any(link.is_owner for link in board_links_to_users if link.username == username):
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title:
            crud.create_card(board_id, title, content)
            return redirect(url_for("board.handle", board_id=board_id), 303)
        else:
            flash('Title is required')

    return render_template('card/create.html', board_id=board_id)


@bp.route('/<int:board_id>/cards/<int:card_id>', methods=['GET', 'POST'])
@jwt_required()
def handle(board_id, card_id):
    card = crud.get_card(board_id, card_id)

    if not card:
        abort(404)

    username = get_jwt_identity()
    user_link_to_board = crud.get_user_link_to_board(board_id, username)

    if not user_link_to_board:
        abort(403)

    if request.method == 'POST':
        operation = request.form['operation']

        if operation == 'DELETE':

            if user_link_to_board.is_owner:
                crud.delete_card(card)
                return redirect(url_for("board.handle", board_id=board_id), 303)
            else:
                abort(403)

        elif operation in ('MOVE_LEFT', 'MOVE_RIGHT'):
            try:
                crud.move_card(card, operation)
            except ValueError:
                abort(400)
            return redirect(url_for("board.handle", board_id=board_id), 303)

        elif operation == 'EDIT':
            if not user_link_to_board.is_owner:
                abort(403)

            title = request.form['title']
            content = request.form['content']

            if not title:
                crud.edit_card(card, content=content)
                flash('Saved, but the title can not be empty')
            else:
                crud.edit_card(card, title=title, content=content)
                flash('Saved')
        else:
            abort(400)

    return render_template(
        'card/view.html',
        card=card,
        board_id=board_id,
        user_info=user_link_to_board
    )
