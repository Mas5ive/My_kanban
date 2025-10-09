// Base URL for API requests
const API_BASE_URL = '/api/v1';

class APIError extends Error {
    constructor(message) {
        super(message);
        this.name = 'APIError';
    }
}

async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const method = options.method ? options.method.toUpperCase() : 'GET';

    if (!['GET', 'HEAD', 'OPTIONS', 'TRACE'].includes(method)) {
        options.headers = {
            'X-CSRFToken': csrfToken,
        };
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        let errorData = await response.json();
        let message = errorData.message || `HTTP error! status: ${response.status}`;
        alert(message);
        throw new APIError(message);
    }

    return response.json();
}

// --- Board related API calls ---

export async function createBoard(form) {
    const formData = new FormData(form);
    return apiFetch('/boards/', {
        method: 'POST',
        body: formData,
    });
}

export async function deleteBoard(boardId) {
    return apiFetch(`/boards/${boardId}`, {
        method: 'DELETE',
    });
}

// --- Card related API calls ---

export async function createCard(boardId, form) {
    const formData = new FormData(form);
    return apiFetch(`/boards/${boardId}/cards/`, {
        method: 'POST',
        body: formData,
    });
}

export async function editCard(boardId, cardId, form) {
    const formData = new FormData(form);
    return apiFetch(`/boards/${boardId}/cards/${cardId}`, {
        method: 'POST',
        body: formData,
    });
}

export async function moveCard(boardId, cardId, operation) {
    const formData = new FormData();
    formData.append('operation', operation);
    return apiFetch(`/boards/${boardId}/cards/${cardId}`, {
        method: 'POST',
        body: formData,
    });
}

export async function deleteCard(boardId, cardId) {
    return apiFetch(`/boards/${boardId}/cards/${cardId}`, {
        method: 'DELETE',
    });
}

// --- Comment related API calls ---

export async function getComments(boardId, cardId) {
    return apiFetch(`/boards/${boardId}/cards/${cardId}/comments/`);
}

export async function createComment(boardId, cardId, form) {
    const formData = new FormData(form);
    return apiFetch(`/boards/${boardId}/cards/${cardId}/comments/`, {
        method: 'POST',
        body: formData,
    });
}

export async function deleteComment(boardId, cardId, commentId) {
    return apiFetch(`/boards/${boardId}/cards/${cardId}/comments/${commentId}`, {
        method: 'DELETE',
    });
}

// --- Profile related API calls ---

export async function getProfileBoards() {
    return apiFetch('/profile/boards');
}

export async function getProfileInvitations() {
    return apiFetch('/profile/invitations');
}

// --- Membership related API calls ---

export async function processInvitation(form) {
    const formData = new FormData(form);
    return apiFetch('/profile/invitations', {
        method: 'POST',
        body: formData,
    });
}

export async function inviteMember(boardId, form) {
    const formData = new FormData(form);
    return apiFetch(`/boards/${boardId}/invitations`, {
        method: 'POST',
        body: formData,
    });
}

export async function deleteMember(boardId, username) {
    return apiFetch(`/boards/${boardId}/users/${username}`, {
        method: 'DELETE',
    });
}