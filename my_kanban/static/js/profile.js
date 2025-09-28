import { getProfileBoards, getProfileInvitations, processInvitation, createBoard } from './apiService.js';

function createBoardElement(board) {
    const form = document.createElement('form');
    form.action = `/boards/${board.id}`;
    form.method = 'get';

    const button = document.createElement('button');
    button.className = 'board-button';
    button.textContent = board.title;

    form.appendChild(button);
    return form;
}

function createInvitationElement(invitation) {
    const container = document.createElement('div');
    container.className = 'line-block';
    container.textContent = `${invitation.sender} invites you to "${invitation.board_title}" `;

    ['reject', 'accept'].forEach(operation => {
        const form = document.createElement('form');
        form.className = 'invitation-form';
        form.innerHTML = `
            <input type="hidden" name="board" value="${invitation.board_id}">
            <input type="hidden" name="operation" value="${operation}">
            <button class="transparent-button" type="submit">${operation}</button>
        `;
        container.appendChild(form);
    });
    return container;
}

function renderBoards(boardsData) {
    ['owner', 'member'].forEach(key => {
        const container = document.getElementById(`${key}-boards-container`);
        const section = document.getElementById(`${key}-boards-section`);

        if (!container || !section) return;

        container.innerHTML = '';
        section.style.display = 'none';

        if (boardsData[`${key}_boards`].length > 0) {
            section.style.display = 'block';
            boardsData[`${key}_boards`].forEach(board => container.appendChild(createBoardElement(board)));
        }
    });
}

function renderInvitations(invitationsData) {
    const container = document.getElementById('invitations-container');
    const section = document.getElementById('invitations-section');

    if (!container || !section) return;

    container.innerHTML = '';
    section.style.display = 'none';

    if (invitationsData.length > 0) {
        section.style.display = 'block';
        invitationsData.forEach(inv => container.appendChild(createInvitationElement(inv)));
    }
}


document.addEventListener('DOMContentLoaded', async () => {
    const boardsData = await getProfileBoards();
    renderBoards(boardsData);
    const invitationsData = await getProfileInvitations();
    renderInvitations(invitationsData);

    // Event delegation for invitation forms (Accept/Reject)
    const invitationsContainer = document.getElementById('invitations-container');
    if (invitationsContainer) {
        invitationsContainer.addEventListener('submit', async (event) => {

            if (!event.target.classList.contains('invitation-form')) {
                return;
            }

            event.preventDefault();
            const form = event.target;
            await processInvitation(form);
            const updatedInvitations = await getProfileInvitations();
            renderInvitations(updatedInvitations);
            const formData = new FormData(form);

            if (formData.get('operation') === 'accept') {
                const updatedBoards = await getProfileBoards();
                renderBoards(updatedBoards);
            }
        });
    }

    // Event listener for creating a new board
    document.getElementById('create-board-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        await createBoard(form);
        const updatedBoards = await getProfileBoards();
        renderBoards(updatedBoards);
        form.reset();
    });
});