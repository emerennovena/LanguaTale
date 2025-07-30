from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, Language
from django.contrib.auth import login
from .forms import CustomSignUpForm
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from gtts import gTTS
import io

def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'welcome.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    stories = Story.objects.all().prefetch_related('available_languages')
    context = {
        'stories': stories,
        'username': request.user.username,
    }
    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomSignUpForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
    }
    return render(request, 'account.html', context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def play_story(request, story_id, language_id):
    story = get_object_or_404(Story, pk=story_id)
    language = get_object_or_404(Language, pk=language_id)

    ink_json = None
    error_message = None

    if story.ink_json_content:
        language_id_str = str(language.id)
        ink_json = story.ink_json_content.get(language_id_str)

        if not ink_json:
            error_message = f"Ink story content not available for {language.name} (ID: {language.id})"
    else:
        error_message = "No Ink JSON content found for this story."

    context = {
        'story': story,
        'language': language,
        'ink_json_content': ink_json,
        'error_message': error_message,
    }
    return render(request, 'play_story.html', context)

@login_required(login_url='login')
def get_ink_json(request, story_id, language_id):
    story = get_object_or_404(Story, pk=story_id)
    language = get_object_or_404(Language, pk=language_id)

    if story.ink_json_content:
        language_id_str = str(language.id)
        ink_json = story.ink_json_content.get(language_id_str)
        if ink_json:
            return JsonResponse(ink_json)
        else:
            return JsonResponse({'error': f'Ink JSON content not found for language ID {language_id_str}.'}, status=404)
    else:
        return JsonResponse({'error': 'No Ink JSON content found for this story.'}, status=404)

@csrf_exempt
def generate_tts(request, story_id, language_id):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        map_language = {
            1: 'en',
            2: 'id',
        }
        lang_code = map_language.get(language_id, 'en')

        try:
            tts = gTTS(text=text, lang=lang_code)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            return HttpResponse(mp3_fp.read(), content_type='audio/mpeg')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error':'Invalid method'}, status=405)