from typing import Any

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import Row, select

from my_kanban import sqla

from .data.models import Card, user_board

bp = Blueprint('card', __name__, url_prefix='/boards')


def get_board_info(board_id: int, username: str) -> Row[Any]:
    board_info = sqla.session.execute(
        select(user_board).
        where(user_board.c.board_id == board_id, user_board.c.username == username)
    ).one_or_none()

    if not board_info:
        abort(403)
    return board_info


def get_card(board_id: int, card_id: int) -> Card:
    card = sqla.session.execute(
        select(Card).
        where(Card.board_id == board_id, Card.id == card_id)
    ).scalar_one_or_none()

    if not card:
        abort(404)
    return card


def delete_card(card: Card, board_info: Row[Any]) -> None:
    if not board_info.is_owner:
        abort(403)
    sqla.session.delete(card)
    sqla.session.commit()


def move_card(card: Card, card_status: str, operation: str) -> None:
    match card_status, operation:
        case '0', 'MOVE_RIGHT':
            card.status = 1
        case '1', 'MOVE_LEFT':
            card.status = 0
        case '1', 'MOVE_RIGHT':
            card.status = 2
        case '2', 'MOVE_LEFT':
            card.status = 1
        case _:
            abort(400)

    sqla.session.commit()


def edit_card(card: Card, title: str, content: str, board_info: Row[Any]) -> None:
    if not board_info.is_owner:
        abort(403)

    if not title:
        flash('Title is required')
    else:
        card.title = title

    card.content = content
    sqla.session.commit()
    flash('Saved')


@bp.route('/<int:board_id>/cards', methods=['GET', 'POST'])
@jwt_required()
def create(board_id):
    board_info = sqla.session.execute(
        select(user_board).
        where(user_board.c.board_id == board_id)
    ).all()

    if board_info == []:
        abort(404)

    username = get_jwt_identity()
    if not any(info.is_owner for info in board_info if info.username == username):
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title:
            new_card = Card(board_id=board_id, title=title, content=content)
            sqla.session.add(new_card)
            sqla.session.commit()
            return redirect(url_for("board.handle", board_id=board_id), 303)
        else:
            flash('Title is required')

    return render_template('card/create.html', board_id=board_id)


@bp.route('/<int:board_id>/cards/<int:card_id>', methods=['GET', 'POST'])
@jwt_required()
def handle(board_id, card_id):
    card = get_card(board_id, card_id)
    username = get_jwt_identity()
    board_info = get_board_info(board_id, username)

    if request.method == 'POST':
        operation = request.form['operation']
        if operation == 'DELETE':
            delete_card(card, user_info.is_owner)
            return redirect(url_for("board.handle", board_id=board_id), 303)
        elif 'MOVE' in operation:
            move_card(card, request.form['card_status'], operation)
            return redirect(url_for("board.handle", board_id=board_id), 303)
        elif operation == 'EDIT':
            edit_card(card, request.form['title'], request.form['content'], board_info)
        else:
            abort(400)

    return render_template(
        'card/view.html',
        card=card,
        board_id=board_id,
        board_info=board_info
    )