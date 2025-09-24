function createCommentElement(comment, boardId, cardId, currentUsername) {
    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment';
    commentDiv.dataset.commentId = comment.id;

    const date = new Date(comment.date).toLocaleString('sv-SE', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });

    const authorP = document.createElement('p');
    authorP.textContent = `${comment.author} (${formattedDate})`;

    const contentP = document.createElement('p');
    contentP.textContent = comment.content;
    contentP.style.whiteSpace = 'pre-wrap';

    commentDiv.appendChild(authorP);
    commentDiv.appendChild(contentP);

    if (comment.author === currentUsername) {
        const deleteForm = document.createElement('form');
        deleteForm.className = 'delete-comment-form';
        deleteForm.dataset.boardId = boardId;
        deleteForm.dataset.cardId = cardId;
        deleteForm.dataset.commentId = comment.id;
        deleteForm.innerHTML = `
            <button class="delete-comment-button">Delete</button>
            <div style="clear: both;"></div>
        `;
        commentDiv.appendChild(deleteForm);
    }

    return commentDiv;
}

async function fetchAndRenderComments(commentsContainer, boardId, cardId, currentUsername) {
    try {
        const response = await fetch(`/api/v1/boards/${boardId}/cards/${cardId}/comments/`);
        if (!response.ok) {
            throw new Error('Failed to fetch comments');
        }
        const comments = await response.json();
        commentsContainer.innerHTML = ''
        comments.forEach(comment => {
            const commentElement = createCommentElement(comment, boardId, cardId, currentUsername);
            commentsContainer.appendChild(commentElement);
        });
    } catch (error) {
        console.error('Error fetching comments:', error);
        alert('Could not load comments.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const commentsSection = document.querySelector('.comments');
    if (!commentsSection) return;

    const commentsContainer = document.querySelector('.comments .scrollable');
    const { boardId, cardId, currentUsername } = commentsContainer.dataset;

    if (commentsContainer && boardId && cardId && currentUsername) {
        fetchAndRenderComments(commentsContainer, boardId, cardId, currentUsername);
    }

    const createCommentForm = document.getElementById('create-comment-form');
    if (createCommentForm) {
        createCommentForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);

            try {
                const response = await fetch(`/api/v1/boards/${boardId}/cards/${cardId}/comments/`, {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    form.reset();
                    await fetchAndRenderComments(commentsContainer, boardId, cardId, currentUsername);
                } else {
                    const errorData = await response.json();
                    alert(errorData.message || 'Failed to create comment.');
                }
            } catch (error) {
                console.error('Error creating comment:', error);
                alert('A network error occurred. Please try again.');
            }
        });
    }

    if (commentsContainer) {
        commentsContainer.addEventListener('submit', async (event) => {
            if (!event.target.classList.contains('delete-comment-form')) return;

            event.preventDefault();
            const form = event.target;
            const { boardId, cardId, commentId } = form.dataset;

            const response = await fetch(`/api/v1/boards/${boardId}/cards/${cardId}/comments/${commentId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                form.closest('.comment').remove();
            } else {
                const errorData = await response.json();
                alert(errorData.message || 'Failed to delete comment.');
            }
        });
    }
});