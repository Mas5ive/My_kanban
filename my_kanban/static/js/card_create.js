document.addEventListener('DOMContentLoaded', () => {
    const createCardForm = document.getElementById('create-card-form');
    if (createCardForm) {
        createCardForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const boardId = form.dataset.boardId;

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/cards/`, {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();

                if (response.ok) {
                    window.location.href = `/boards/${boardId}`;
                } else {
                    alert(result.message || 'Failed to create card.');
                }
            } catch (error) {
                console.error('Error creating card:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }
});