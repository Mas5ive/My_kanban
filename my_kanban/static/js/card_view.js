document.addEventListener('DOMContentLoaded', () => {
    const deleteCardForm = document.getElementById('delete-card-form');

    if (deleteCardForm) {
        deleteCardForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            if (!confirm('Are you sure you want to delete this card?')) {
                return;
            }

            const form = event.target;
            const boardId = form.dataset.boardId;
            const cardId = form.dataset.cardId;

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/cards/${cardId}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    window.location.href = `/boards/${boardId}`;
                } else {
                    const result = await response.json();
                    alert(result.message || 'Failed to delete card.');
                }
            } catch (error) {
                console.error('Error deleting card:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }

    const editCardForm = document.getElementById('edit-card-form');
    if (editCardForm) {
        editCardForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const boardId = form.dataset.boardId;
            const cardId = form.dataset.cardId;

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/cards/${cardId}`, {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();
                alert(result.message || 'An unknown error occurred.');

            } catch (error) {
                console.error('Error editing card:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }

});