function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return '';
}

function onStoryCompleted(storyId, languageId) {
    console.log(`DEBUG: Completing story ${storyId} in language ${languageId}`);

    fetch(`/api/story_completed/${storyId}/${languageId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ completed: true }),
    })
        .then(response => {
            console.log('DEBUG: Response status', response.status);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('DEBUG: Completion logged:', data);
            if (data.success) {
                console.log('DEBUG: Story completion saved successfully.');
            }
        })
        .catch(err => console.error('DEBUG: Error logging completion:', err));

    if (typeof showConfetti === 'function') {
        showConfetti();
    }
}
