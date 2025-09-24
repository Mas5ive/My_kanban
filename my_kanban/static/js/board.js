document.addEventListener('DOMContentLoaded', () => {

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