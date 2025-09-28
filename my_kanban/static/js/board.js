import { moveCard, inviteMember, deleteMember, deleteBoard } from './apiService.js';
import { nl2br } from './utils.js';

function createCardElement(cardId, cardTitle, boardId, columnIndex) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card';
    cardDiv.dataset.cardId = cardId;

    const openForm = document.createElement('form');
    openForm.action = `/boards/${boardId}/cards/${cardId}`;
    openForm.method = 'get';
    openForm.className = 'flex-grow-rest';

    const openButton = document.createElement('button');
    openButton.className = 'open-card-button';
    openButton.innerHTML = nl2br(cardTitle);
    openForm.appendChild(openButton);

    const createMoveButton = (operation, text) => {
        const button = document.createElement('button');
        button.className = 'move-card-button flex-20';
        button.dataset.operation = operation;
        button.dataset.boardId = boardId;
        button.dataset.cardId = cardId;
        button.innerHTML = text;
        return button;
    };

    // columnIndex: 0 = Backlog, 1 = In progress, 2 = Done
    if (columnIndex === 0) { // Backlog
        cardDiv.appendChild(openForm);
        cardDiv.appendChild(createMoveButton('MOVE_RIGHT', '=&gt;'));
    } else if (columnIndex === 1) { // In progress
        cardDiv.appendChild(createMoveButton('MOVE_LEFT', '&#60;='));
        cardDiv.appendChild(openForm);
        cardDiv.appendChild(createMoveButton('MOVE_RIGHT', '=&gt;'));
    } else if (columnIndex === 2) { // Done
        cardDiv.appendChild(createMoveButton('MOVE_LEFT', '&#60;='));
        cardDiv.appendChild(openForm);
    }

    return cardDiv;
}

function updateColumnCounter(column) {
    const counter = column.querySelector('h2');
    const cardCount = column.querySelectorAll('.card').length;
    counter.textContent = counter.textContent.replace(/\[\d+\]/, `[${cardCount}]`);
}


document.addEventListener('DOMContentLoaded', () => {

    // Event listener for moving cards
    const board = document.querySelector('.board');
    if (board) {
        board.addEventListener('click', async (event) => {

            if (!event.target.classList.contains('move-card-button')) {
                return;
            }

            event.preventDefault();
            const button = event.target;
            const { boardId, cardId, operation } = button.dataset;
            await moveCard(boardId, cardId, operation);
            const oldCardElement = button.closest('.card');
            const cardTitle = oldCardElement.querySelector('.open-card-button').innerHTML;
            const currentColumn = oldCardElement.closest('.column');
            const columns = Array.from(board.querySelectorAll('.column'));
            const currentColumnIndex = columns.indexOf(currentColumn);

            let targetColumnIndex;

            if (operation === 'MOVE_RIGHT') {
                targetColumnIndex = currentColumnIndex + 1;
            } else if (operation === 'MOVE_LEFT') {
                targetColumnIndex = currentColumnIndex - 1;
            }

            const targetColumn = columns[targetColumnIndex];

            if (targetColumn) {
                oldCardElement.remove();
                const newCardElement = createCardElement(cardId, cardTitle, boardId, targetColumnIndex);
                const scrollableArea = targetColumn.querySelector('.scrollable');
                scrollableArea.appendChild(newCardElement);
                updateColumnCounter(currentColumn);
                updateColumnCounter(targetColumn);
            }
        });
    }

    // Event listener for deleting members
    const membersContainer = document.querySelector('.members .scrollable');
    if (membersContainer) {
        membersContainer.addEventListener('click', async (event) => {

            if (!event.target.classList.contains('delete-member-button')) {
                return;
            }

            event.preventDefault();
            const button = event.target;
            const boardId = button.dataset.boardId;
            const username = button.dataset.username;

            if (!confirm(`Are you sure you want to remove ${username} from this board?`)) {
                return;
            }

            await deleteMember(boardId, username);
            button.closest('.member').remove();
        });
    }

    // Event listener for inviting members
    const inviteForm = document.getElementById('invite-form');
    if (inviteForm) {
        inviteForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const form = event.target;
            const boardId = form.dataset.boardId;
            const result = await inviteMember(boardId, form);
            form.reset();
            alert(result.message);
        });
    }

    // Event listener for deleting board
    const deleteBoardButton = document.getElementById('delete-board-button');
    if (deleteBoardButton) {
        deleteBoardButton.addEventListener('click', async (event) => {

            if (!confirm('Are you sure you want to delete this board? This action cannot be undone.')) {
                return;
            }

            event.preventDefault();
            const button = event.target;
            const boardId = button.dataset.boardId;
            await deleteBoard(boardId);
            window.location.href = '/profile';
        });
    }
});