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
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('DEBUG: Completion logged:', data);
            if (data.success) {
                console.log('DEBUG: Story completion saved successfully.');
                return fetch('/api/completed_stories/');
            } else {
                throw new Error('Completion not successful');
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch completed stories');
            return response.json();
        })
        .then(data => {
            updateCompletedStoriesList(data.completed_stories);
        })
        .catch(err => console.error('DEBUG: Error logging completion or fetching completed stories:', err));
}

function updateCompletedStoriesList(completedStories) {
    const container = document.querySelector('.stories-grid');
    if (!container) return;

    container.innerHTML = '';

    if (completedStories.length === 0) {
        container.innerHTML = '<p>No completed stories yet.</p>';
        return;
    }

    completedStories.forEach(cs => {
        const storyCard = document.createElement('div');
        storyCard.classList.add('story-card');

        const titleDiv = document.createElement('div');
        titleDiv.classList.add('story-title');
        titleDiv.textContent = cs.story_title;

        const langButton = document.createElement('button');
        langButton.classList.add('language-button');
        langButton.textContent = cs.language_name || 'Unknown Language';

        storyCard.appendChild(titleDiv);
        storyCard.appendChild(langButton);

        container.appendChild(storyCard);
    });
}
