from collections import defaultdict

from sqlalchemy import Row, Sequence

from my_kanban.models import Board, Card


def get_card_groups(cards: list[Card]) -> dict[int, list[Card]]:
    """Groups a list of cards by their status.

    Args:
        cards: A list of Card objects.

    Returns:
        A dictionary where keys are card statuses (int) and values are lists
        of cards with that status.
    """
    grouped_cards = defaultdict(list)
    for card in cards:
        grouped_cards[card.status].append(card)
    return grouped_cards


def split_boards(boards_info: Sequence[Row]) -> dict[str, list[Board]]:
    """Splits boards into owner- and member-of boards.

    Args:
        boards_info: A sequence of SQLAlchemy Rows, where each row contains
                     a Board object and an is_owner flag.

    Returns:
        A dictionary with two keys: 'owner boards' and 'invitation boards',
        each containing a list of Board objects.
    """
    boards = defaultdict(list)
    for board, is_owner in boards_info:
        if is_owner:
            boards['owner boards'].append(board)
        else:
            boards['invitation boards'].append(board)
    return boards
