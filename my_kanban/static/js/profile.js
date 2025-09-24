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

    const rejectForm = document.createElement('form');
    rejectForm.action = '/api/v1/profile/invitations';
    rejectForm.method = 'post';
    rejectForm.innerHTML = `
                <input type="hidden" name="board" value="${invitation.board_id}">
                <input type="hidden" name="operation" value="reject">
                <button class="transparent-button" type="submit">Reject</button>
            `;

    const acceptForm = document.createElement('form');
    acceptForm.action = '/api/v1/profile/invitations';
    acceptForm.method = 'post';
    acceptForm.innerHTML = `
                <input type="hidden" name="board" value="${invitation.board_id}">
                <input type="hidden" name="operation" value="accept">
                <button class="transparent-button" type="submit">Accept</button>
            `;

    container.appendChild(rejectForm);
    container.appendChild(acceptForm);
    return container;
}

async function fetchAndRenderBoards() {
    const response = await fetch('/api/v1/profile/boards');
    const data = await response.json();

    const ownerContainer = document.getElementById('owner-boards-container');
    if (data.owner_boards.length > 0) {
        document.getElementById('owner-boards-section').style.display = 'block';
        data.owner_boards.forEach(board => ownerContainer.appendChild(createBoardElement(board)));
    }

    const memberContainer = document.getElementById('member-boards-container');
    if (data.member_boards.length > 0) {
        document.getElementById('member-boards-section').style.display = 'block';
        data.member_boards.forEach(board => memberContainer.appendChild(createBoardElement(board)));
    }
}

async function fetchAndRenderInvitations() {
    const response = await fetch('/api/v1/profile/invitations');
    const invitations = await response.json();

    const container = document.getElementById('invitations-container');
    if (invitations.length > 0) {
        document.getElementById('invitations-section').style.display = 'block';
        invitations.forEach(inv => container.appendChild(createInvitationElement(inv)));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderBoards();
    fetchAndRenderInvitations();
});

document.getElementById('invitations-container').addEventListener('submit', async (event) => {
    if (event.target.tagName !== 'FORM') {
        return;
    }
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
        });

        if (response.ok) {
            const invitationsContainer = document.getElementById('invitations-container');
            invitationsContainer.innerHTML = '';
            document.getElementById('invitations-section').style.display = 'none';
            fetchAndRenderInvitations();

            if (formData.get('operation') === 'accept') {
                document.getElementById('owner-boards-container').innerHTML = '';
                document.getElementById('owner-boards-section').style.display = 'none';
                document.getElementById('member-boards-container').innerHTML = '';
                document.getElementById('member-boards-section').style.display = 'none';
                fetchAndRenderBoards();
            }
        } else {
            const errorData = await response.json();
            alert(errorData.message || 'An error occurred while processing the invitation.');
        }
    } catch (error) {
        console.error('Error processing invitation:', error);
        alert('A network error occurred. Please try again.');
    }
});

document.getElementById('create-board-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/api/v1/boards/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            form.reset();
            // Clear and hide board containers before re-fetching
            document.getElementById('owner-boards-container').innerHTML = '';
            document.getElementById('owner-boards-section').style.display = 'none';
            document.getElementById('member-boards-container').innerHTML = '';
            document.getElementById('member-boards-section').style.display = 'none';
            fetchAndRenderBoards();
        } else {
            const errorData = await response.json();
            alert(errorData.message || 'An error occurred while creating the board.');
        }
    } catch (error) {
        console.error('Error creating board:', error);
        alert('A network error occurred. Please try again.');
    }
});