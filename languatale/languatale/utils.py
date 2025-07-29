import re
from gtts import gTTS
from .models import Story, Audio

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def generate_audio_for_story(story_id):
    story = Story.objects.get(id=story_id)
    text = story.ink_json_content.get("content", "")

    if not (text):
        return

    sentences = split_sentences(text)

    for sentence in sentences:
        if not sentence.strip():
            continue

    tts = gTTS(sentence)
    temp_audio = NamedTemporaryFile(delete=True)
    tts.save(temp_audio.name)

    audio_model = Audio(story=story, sentence_text=sentence)
    audio_model.audio_file.save(f"{story.id}_{hash(sentence)}.mp3", File(temp_audio))
    audio_model.save()