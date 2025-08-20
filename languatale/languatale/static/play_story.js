/*
Filename: play_story.js
Author: Emerentia Novena
Date: 2025-08-07
AI Usage Declaration:
- This file contains code generated with the help of AI tools.
- Tools used: ChatGPT
- Date Generated: 2025-07-20
- AI Generated Sections are marked with comments: // [AI-GENERATED]

Reason for AI Assistance:
- InkJS documentation (https://www.npmjs.com/package/inkjs) is very limited and does not provide detailed examples or guidance on integration.
- I was stuck on how to display Ink story content sentence-by-sentence, since InkJS display the whole paragraph.
- Additional challenges included splitting paragraphs into sentences, managing sentence indices, handling UI state changes (play, continue, replay buttons), and smooth scrolling animations.
- No clear or comprehensive examples were made available online, so I used ChatGPT to help generate the logic and code for these features.
- I have reviewed, tested, and fully understand all AI-generated code before including it in this project.

Note:
- Any additional changes made since the original version are student-written.
*/

// [STUDENT-WRITTEN]
document.addEventListener('DOMContentLoaded', function() {
    const storyContainerDiv = document.getElementById('story-container');
    const storyId = storyContainerDiv.dataset.storyId;
    const languageId = storyContainerDiv.dataset.languageId;
    const playButton = document.getElementById('play-button');
    const choicesContainerDiv = document.getElementById('choices-container');

    const modal = document.getElementById('modal-container');
    const helpButton = document.getElementById('help-button');
    const closeModal = document.querySelector('.close');

    let story = null;
    let currentSentences = [];
    let currentSentenceIndex = 0;

    // [STUDENT-WRITTEN]
    helpButton.onclick = function() {
        modal.style.display = "block";
    }
    closeModal.onclick = function(){
        modal.style.display = "none";
    }
    window.onclick = function(event){
        if (event.target == modal){
            modal.style.display = "none";
        }
    }

    // Adapted from Django documentation: https://docs.djangoproject.com/en/5.2/howto/csrf/
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return '';
    }

    // [AI-GENERATED: ChatGPT: 2025-07-20]
    /*
    Notes:
    I struggled with this part because most gTTS examples only showed how to generate MP3 files locally.
    I couldn’t find examples for:

    - Generating TTS with gTTS in Django on-the-fly without saving the MP3 files locally.
    - Streaming it back as a playable audio blob
    - Playing it in-browser using JavaScript’s Audio() object

    I was stuck in figuring out the entire flow with blob handling and audio playback, and failed to find relevant solutions/code examples to support my understanding.
    */
    function playTTS(sentenceText) {
        const url = `/api/tts/${storyId}/${languageId}/`;
        console.log("TTS URL:", url);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken(),
            },
            body: new URLSearchParams({ 'text': sentenceText })
        })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.blob();
            })
            .then(blob => {
                const audioUrl = URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);
                audio.play();
                audio.onended = () => URL.revokeObjectURL(audioUrl);
            })
            .catch(err => {
                console.error('TTS request failed:', err);
            });
    }

    // [STUDENT-WRITTEN]
    const getTagFromRoot = (jsonRoot, tagName) => {
        if (Array.isArray(jsonRoot) && jsonRoot.length > 0 && Array.isArray(jsonRoot[0])) {
            const tagEntry = jsonRoot[0].find(item => typeof item === 'string' && item.includes(`^${tagName}:`));
            if (tagEntry) {
                return tagEntry.replace(/[\^#\/]/g, '').trim();
            }
        }
        return null;
    };

    // [STUDENT-WRITTEN]
    function loadStoryJsonFromHtml() {
        const scriptTag = document.getElementById('ink-json-data');
        if (scriptTag) {
            try {
                return JSON.parse(scriptTag.textContent);
            } catch (e) {
                return null;
            }
        }
        return null;
    }

    // [AI-GENERATED: ChatGPT: 2025-07-20]
    /*
    Notes:
    I used ChatGPT for this part because there are not a lot of InkJS integration examples online.
    The InkJS documentation is not complete and does not show exactly on how to integrate it to other parts. "https://www.npmjs.com/package/inkjs"

    InkJS show the entire paragraphs at once. However, I wanted to display sentences individually (per user clicks),
    but I was stuck and could not find any example of these:

    - Splitting story text into individual sentences using regex
    - Tracking which sentence index to show next
    - Handling button state changes (Play, Continue, Replay)
    - Managing scroll behavior and smooth animations
    */
    function displayNextSentence() {
        choicesContainerDiv.innerHTML = '';
        playButton.style.display = 'block';

        if (!story || typeof story.ContinueMaximally !== 'function') {
            playButton.textContent = 'Play';
            playButton.disabled = false;
            return;
        }

        if (currentSentenceIndex < currentSentences.length) {
            const sentenceText = currentSentences[currentSentenceIndex].trim();
            if (sentenceText) {
                const sentenceElement = document.createElement('div');
                sentenceElement.classList.add('story-sentence-wrapper');

                const textSpan = document.createElement('span');
                textSpan.textContent = sentenceText;
                textSpan.classList.add('story-sentence');

                const audioButton = document.createElement('button');
                audioButton.innerHTML = '<i class="fa fa-volume-up" aria-hidden="true"></i>';
                audioButton.classList.add('tts-button');
                audioButton.title = 'Play audio';
                audioButton.addEventListener('click', ()=>{
                    playTTS(sentenceText);
                });

                sentenceElement.appendChild(textSpan);
                sentenceElement.appendChild(audioButton);
                storyContainerDiv.appendChild(sentenceElement);

                sentenceElement.style.opacity = '0';
                setTimeout(() => {
                    sentenceElement.style.transition = 'opacity 0.7s ease-in';
                    sentenceElement.style.opacity = '1';
                    sentenceElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
                }, 50);
            }
            currentSentenceIndex++;
            playButton.textContent = 'Continue';
            playButton.disabled = false;
        } else {
            if (story.canContinue) {
                const paragraph = story.ContinueMaximally();
                currentSentences = paragraph.trim().split(/(?<=[.!?])\s*(?=[A-Z"'])/g).filter(s => s.trim() !== '');
                currentSentenceIndex = 0;
                if (currentSentences.length > 0) {
                    displayNextSentence();
                } else {
                    handleInkState();
                }
            } else {
                handleInkState();
            }
        }
    }

    // [STUDENT-WRITTEN]
    function handleInkState() {
        if (!story) return;

        if (story.currentChoices.length > 0) {
            displayChoices();
        } else if (!story.canContinue && story.currentChoices.length === 0) {
            storyContainerDiv.innerHTML += '<p class="story-end-message">Congratulations! You have reached the end of this story.</p>';
            playButton.textContent = 'Replay';
            playButton.style.display = 'block';
            playButton.disabled = false;

            onStoryCompleted(storyId, languageId);

        } else {
            playButton.textContent = 'Continue';
            playButton.style.display = 'block';
            playButton.disabled = false;
        }
    }

    // [STUDENT-WRITTEN]
    function displayChoices() {
        if (!story) return;

        choicesContainerDiv.innerHTML = '';
        playButton.style.display = 'none';

        story.currentChoices.forEach(choice => {
            const choiceElement = document.createElement('div');
            choiceElement.classList.add('story-choice-button');
            choiceElement.textContent = choice.text;
            choiceElement.addEventListener('click', function() {
                story.ChooseChoiceIndex(choice.index);
                choicesContainerDiv.innerHTML = '';
                const paragraph = story.ContinueMaximally();
                currentSentences = paragraph.trim().split(/(?<=[.!?])\s*(?=[A-Z"'])/g).filter(s => s.trim() !== '');
                currentSentenceIndex = 0;
                displayNextSentence();
            });
            choicesContainerDiv.appendChild(choiceElement);
        });
    }

    // [STUDENT-WRITTEN]
    playButton.addEventListener('click', function() {
        if (playButton.textContent === 'Replay') {
            storyContainerDiv.innerHTML = '';
            choicesContainerDiv.innerHTML = '';
            currentSentences = [];
            currentSentenceIndex = 0;
        }

        if (typeof inkjs === 'undefined' || typeof inkjs.Story === 'undefined') {
            playButton.textContent = 'Play';
            playButton.disabled = true;
            return;
        }

        if (!story || playButton.textContent === 'Replay' || playButton.textContent === 'Play') {
            storyContainerDiv.innerHTML = '';
            choicesContainerDiv.innerHTML = '';
            const storyJson = loadStoryJsonFromHtml();
            if (storyJson) {
                try {
                    story = new inkjs.Story(storyJson);
                } catch (e) {
                    story = null;
                }

                if (story && typeof story.ContinueMaximally === 'function') {
                    const titleText = getTagFromRoot(storyJson.root, 'title');
                    if (titleText) {
                        const h1Element = document.querySelector('h1');
                        if (h1Element) {
                            h1Element.textContent = titleText.replace('title:', '').trim();
                        }
                    }

                    const authorText = getTagFromRoot(storyJson.root, 'author');
                    if (authorText) {
                        let authorElement = document.querySelector('.story-author-display');
                        if (!authorElement) {
                            authorElement = document.createElement('p');
                            authorElement.classList.add('story-author-display');
                            const h1Element = document.querySelector('h1');
                            if (h1Element) {
                                h1Element.insertAdjacentElement('afterend', authorElement);
                            } else {
                                storyContainerDiv.insertAdjacentElement('beforebegin', authorElement);
                            }
                        }
                        authorElement.textContent = `by ${authorText.replace('author:', '').trim()}`;
                    }

                    const paragraph = story.ContinueMaximally();
                    currentSentences = paragraph.trim().split(/(?<=[.!?])\s*(?=[A-Z"'])/g).filter(s => s.trim() !== '');
                    currentSentenceIndex = 0;
                    displayNextSentence();
                } else {
                    playButton.textContent = 'Play';
                    playButton.disabled = false;
                }
            } else {
                playButton.textContent = 'Play';
                playButton.disabled = false;
            }
        } else {
            displayNextSentence();
        }
    });

    playButton.textContent = 'Play';
    playButton.disabled = false;
    storyContainerDiv.innerHTML = '';
    choicesContainerDiv.innerHTML = '';

    const initialStoryJson = loadStoryJsonFromHtml();
    if (initialStoryJson) {
        const titleText = getTagFromRoot(initialStoryJson.root, 'title');
        if (titleText) {
            const h1Element = document.querySelector('h1');
            if (h1Element) {
                h1Element.textContent = titleText.replace('title:', '').trim();
            }
        }

        const authorText = getTagFromRoot(initialStoryJson.root, 'author');
        if (authorText) {
            let authorElement = document.querySelector('.story-author-display');
            if (!authorElement) {
                authorElement = document.createElement('p');
                authorElement.classList.add('story-author-display');
                const h1Element = document.querySelector('h1');
                if (h1Element) {
                    h1Element.insertAdjacentElement('afterend', authorElement);
                } else {
                    storyContainerDiv.insertAdjacentElement('beforebegin', authorElement);
                }
            }
            authorElement.textContent = `by ${authorText.replace('author:', '').trim()}`;
        }
    } else {
        playButton.style.display = 'none';
    }

});
