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
    openButton.innerHTML = cardTitle.replace(/\n/g, "<br>");
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

    const board = document.querySelector('.board');
    if (board) {
        board.addEventListener('click', async (event) => {
            if (!event.target.classList.contains('move-card-button')) {
                return;
            }

            event.preventDefault();
            const button = event.target;
            const { boardId, cardId, operation } = button.dataset;

            const formData = new FormData();
            formData.append('operation', operation);

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/cards/${cardId}`, {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
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
                } else {
                    const errorData = await response.json();
                    alert(errorData.message || 'Failed to move card.');
                }
            } catch (error) {
                console.error('Error moving card:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }


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

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/users/${username}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    button.closest('.member').remove();
                } else {
                    const errorData = await response.json();
                    alert(errorData.message || 'Failed to remove member.');
                }
            } catch (error) {
                console.error('Error removing member:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }

    const inviteForm = document.getElementById('invite-form');
    if (inviteForm) {
        inviteForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const boardId = form.dataset.boardId;

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/invitations`, {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    form.reset();
                } else {
                    alert(result.message || 'Failed to send invitation.');
                }
            } catch (error) {
                console.error('Error sending invitation:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }

    const deleteBoardButton = document.getElementById('delete-board-button');
    if (deleteBoardButton) {
        deleteBoardButton.addEventListener('click', async (event) => {

            event.preventDefault();
            const button = event.target;
            const boardId = button.dataset.boardId;

            if (!confirm('Are you sure you want to delete this board? This action cannot be undone.')) {
                return;
            }

            try {
                const response = await fetch(`/api/v1/boards/${boardId}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    window.location.href = '/profile';
                } else {
                    const errorData = await response.json();
                    alert(errorData.message || 'Failed to delete board.');
                }
            } catch (error) {
                console.error('Error deleting board:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }
});