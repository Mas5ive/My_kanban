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
    rejectForm.action = "{{ url_for('membership.pick_invitation') }}";
    rejectForm.method = 'post';
    rejectForm.innerHTML = `
                <input type="hidden" name="board" value="${invitation.board_id}">
                <input type="hidden" name="operation" value="reject">
                <button class="transparent-button" type="submit">Reject</button>
            `;

    const acceptForm = document.createElement('form');
    acceptForm.action = "{{ url_for('membership.pick_invitation') }}";
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