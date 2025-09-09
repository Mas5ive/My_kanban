from typing import Any, Tuple

from sqlalchemy import Row, Sequence, select
from sqlalchemy.orm import joinedload, selectinload
from werkzeug.security import generate_password_hash

from my_kanban import sqla
from my_kanban.models import Board, Card, Comment, Invitation, User, user_board


def create_user(username: str, password: str) -> None:
    user = User(
        name=username,
        psw_hash=generate_password_hash(password)
    )
    sqla.session.add(user)
    sqla.session.commit()


def get_user_by_name(username: str) -> User | None:
    return sqla.session.query(User).filter(User.name == username).first()


def create_board(board_title: str, username: str) -> None:
    with sqla.session.begin_nested():
        new_board = Board(title=board_title)
        sqla.session.add(new_board)
        sqla.session.flush()

        sqla.session.execute(
            user_board.insert().
            values(username=username, board_id=new_board.id, is_owner=1)
        )
    sqla.session.commit()


def get_board(board_id: int) -> Board | None:
    return sqla.session.execute(
        select(Board).
        options(joinedload(Board.users), selectinload(Board.cards)).
        where(Board.id == board_id)
    ).unique().scalar_one_or_none()


def delete_board(board: Board) -> None:
    sqla.session.delete(board)
    sqla.session.commit()


def get_user_link_to_board(board_id: int, username: str) -> Row[Any] | None:
    return sqla.session.execute(
        select(user_board).
        where(user_board.c.board_id == board_id, user_board.c.username == username)
    ).one_or_none()


def get_user_boards(username: str) -> Sequence[Row]:
    return sqla.session.execute(
        select(Board, user_board.c.is_owner).
        join(user_board, user_board.c.board_id == Board.id).
        where(user_board.c.username == username)
    ).all()


def get_board_links_to_users(board_id: int) -> Sequence[Row[Any]]:
    return sqla.session.execute(
        select(user_board).
        where(user_board.c.board_id == board_id)
    ).all()


def create_invitation(board_id: int, recipient: str, sender: str) -> None:
    invitation = Invitation(
        user_recipient=recipient,
        board_id=board_id,
        user_sender=sender
    )
    sqla.session.add(invitation)
    sqla.session.commit()


def get_invitation_by_recipient(board_id: int, recipient: str) -> Invitation | None:
    return sqla.session.execute(
        select(Invitation).
        where(Invitation.board_id == board_id, Invitation.user_recipient == recipient)
    ).scalar_one_or_none()


def get_recipient_invitations(recipient: str) -> Sequence[Row[Tuple[Invitation, str]]]:
    return sqla.session.execute(
        select(Invitation, Board.title).
        join(Board, Invitation.board_id == Board.id).
        where(Invitation.user_recipient == recipient)
    ).all()


def delete_invitation(invitation: Invitation) -> None:
    sqla.session.delete(invitation)
    sqla.session.commit()


def create_member(invitation: Invitation) -> None:
    with sqla.session.begin_nested():
        sqla.session.delete(invitation)
        sqla.session.execute(
            user_board.insert().values(username=invitation.user_recipient, board_id=invitation.board_id)
        )
    sqla.session.commit()


def delete_member(board_id: int, member: str) -> None:
    sqla.session.execute(
        user_board.delete().
        where(user_board.c.username == member, user_board.c.board_id == board_id)
    )
    sqla.session.commit()


def create_card(board_id: int, title: str, content: str) -> None:
    card = Card(board_id=board_id, title=title, content=content)
    sqla.session.add(card)
    sqla.session.commit()


def get_card(board_id: int, card_id: int) -> Card | None:
    return sqla.session.execute(
        select(Card).
        options(selectinload(Card.comments), joinedload(Card.board)).
        where(Card.id == card_id, Card.board_id == board_id)
    ).scalar_one_or_none()


def move_card(card: Card, operation: str) -> None:
    match card.status, operation:
        case 0, 'MOVE_RIGHT':
            card.status = 1
        case 1, 'MOVE_LEFT':
            card.status = 0
        case 1, 'MOVE_RIGHT':
            card.status = 2
        case 2, 'MOVE_LEFT':
            card.status = 1
        case _:
            raise ValueError('Invalid card status or operation')

    sqla.session.commit()


def edit_card(card: Card, title: str | None = None, content: str | None = None) -> None:
    if title is not None:
        card.title = title

    if content is not None:
        card.content = content

    sqla.session.commit()


def delete_card(card: Card) -> None:
    sqla.session.delete(card)
    sqla.session.commit()


def create_comment(card_id: int, author: str, content: str) -> None:
    comment = Comment(card_id=card_id, author=author, content=content)
    sqla.session.add(comment)
    sqla.session.commit()


def get_comment(comment_id: int) -> Comment | None:
    return sqla.session.get(Comment, comment_id)


def delete_comment(comment: Comment) -> None:
    sqla.session.delete(comment)
    sqla.session.commit()
