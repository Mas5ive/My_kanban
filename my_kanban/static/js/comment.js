import { getComments, createComment, deleteComment } from './apiService.js';
import { formatDate, nl2br } from './utils.js';

function createCommentElement(comment, boardId, cardId, currentUsername) {
    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment';
    commentDiv.dataset.commentId = comment.id;
    const formattedDate = formatDate(comment.date);

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

function renderComments(commentsContainer, comments, boardId, cardId, currentUsername) {
    commentsContainer.innerHTML = ''
    comments.forEach(comment => {
        const commentElement = createCommentElement(comment, boardId, cardId, currentUsername);
        commentsContainer.appendChild(commentElement);
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const commentsSection = document.querySelector('.comments');

    if (!commentsSection) return;

    const commentsContainer = document.querySelector('.comments .scrollable');
    const { boardId, cardId, currentUsername } = commentsContainer.dataset;
    const comments = await getComments(boardId, cardId);
    renderComments(commentsContainer, comments, boardId, cardId, currentUsername);


    // Event listener for creating a new comment
    const createCommentForm = document.getElementById('create-comment-form');
    if (createCommentForm) {
        createCommentForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const form = event.target;
            await createComment(boardId, cardId, form);
            form.reset();
            const comments = await getComments(boardId, cardId);
            renderComments(commentsContainer, comments, boardId, cardId, currentUsername);
        });
    }

    // Event listener for deleting a comment
    if (commentsContainer) {
        commentsContainer.addEventListener('submit', async (event) => {

            if (!event.target.classList.contains('delete-comment-form')) return;

            event.preventDefault();
            const form = event.target;
            const { boardId, cardId, commentId } = form.dataset;
            await deleteComment(boardId, cardId, commentId);
            form.closest('.comment').remove();
        });
    }
});