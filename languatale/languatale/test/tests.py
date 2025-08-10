import json
from unittest.mock import patch, Mock

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from languatale.forms import CustomSignUpForm, CustomLoginForm
from languatale.models import Story, Language, CompletedStory
from languatale.views import generate_tts, story_completed

#######################################################################################################################
# FORM TESTING SECTION
# Tests for custom Django forms
#######################################################################################################################

class CustomSignUpFormTest(TestCase):
    def test_form_has_correct_fields(self):
        form = CustomSignUpForm()
        expected_fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'email@example.com',
            'first_name': 'Emerentia',
            'last_name': 'Novena',
            'password1': 'pass345@EN',
            'password2': 'pass345@EN'
        }
        form = CustomSignUpForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_missing_email(self):
        form_data = {
            'username': 'testuser',
            'password1': 'pass345@EN',
            'password2': 'pass345@EN',
            # no email
        }
        form = CustomSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'email@example.com',
            'first_name': 'Emerentia',
            'last_name': 'Novena',
            'password1': 'pass12345@EN',
            'password2': 'pass34521@EN'
        }
        form = CustomSignUpForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_creates_user(self):
        form_data = {
            'username': 'testuser',
            'email': 'email@example.com',
            'first_name': 'Emerentia',
            'last_name': 'Novena',
            'password1': 'pass345@EN',
            'password2': 'pass345@EN'
        }
        form = CustomSignUpForm(data=form_data)

        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'email@example.com')
        self.assertEqual(user.first_name, 'Emerentia')
        self.assertEqual(user.last_name, 'Novena')
        self.assertTrue(user.check_password('pass345@EN'))


    def test_form_widget_classes(self):
        form = CustomSignUpForm()
        self.assertEqual(form.fields['email'].widget.attrs['class'], 'input-field')
        self.assertEqual(form.fields['first_name'].widget.attrs['class'], 'input-field')
        self.assertEqual(form.fields['last_name'].widget.attrs['class'], 'input-field')

# Test CustomLoginForm
class CustomLoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_form_widget_classes(self):
        form = CustomLoginForm()

        self.assertEqual(form.fields['username'].widget.attrs['class'], 'input-field')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'input-field')

    def test_form_valid_login(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = CustomLoginForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid_login(self):
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        form = CustomLoginForm(data=form_data)

        self.assertFalse(form.is_valid())

#######################################################################################################################
# VIEW TESTING SECTION
# Tests for Django views to ensure correct page rendering and user interactions
#######################################################################################################################

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='email@example.com',
            first_name='Emerentia',
            last_name='Novena'
        )

        # Create test data
        self.language = Language.objects.create(id=1, name='English')
        self.story = Story.objects.create(
            id=1,
            title='Test Story',
            ink_json_content={'1': {'content': 'Test story content'}}
        )

    def test_welcome_view_unauthenticated(self):
        # Test welcome page for unauthenticated users
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')

    # Test welcome view redirects authenticated users to home
    def test_welcome_view_authenticated_redirects(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('welcome'))
        self.assertRedirects(response, reverse('home'))

    # Test home view requires login
    def test_home_view_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Test home view for authenticated user
    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('stories', response.context)
        self.assertEqual(response.context['username'], 'testuser')

    # Test sign up view GET request
    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], CustomSignUpForm)

    # Test sign up view with valid POST data
    def test_signup_view_post_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'email@example.com',
            'first_name': 'Emerentia',
            'last_name': 'Novena',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('signup'), data=form_data)

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    # Test sign up view with invalid POST data
    def test_signup_view_post_invalid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'differentpassword123'
        }
        response = self.client.post(reverse('signup'), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFalse(response.context['form'].is_valid())

    # Test account view for authenticated user
    def test_account_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
        self.assertEqual(response.context['username'], 'testuser')
        self.assertEqual(response.context['email'], 'email@example.com')
        self.assertEqual(response.context['first_name'], 'Emerentia')
        self.assertEqual(response.context['last_name'], 'Novena')

    # Test play_story view
    def test_play_story_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('play_story', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'play_story.html')
        self.assertEqual(response.context['story'], self.story)
        self.assertEqual(response.context['language'], self.language)

    # Test generate_tts_view
    @patch('languatale.views.gTTS')
    def test_generate_tts_view(self, mock_gtts):
        mock_tts_instance = Mock()
        mock_gtts.return_value = mock_tts_instance

        # Mock the write_to_fp method
        def mock_write_to_fp(fp):
            fp.write(b'fake_audio_data')
        mock_tts_instance.write_to_fp = mock_write_to_fp

        url = reverse('generate_tts', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.post(url, data={'text': 'Hello world'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'audio/mpeg')
        mock_gtts.assert_called_once_with(text='Hello world', lang='en')

    # Test generate_tts_view with no text
    def test_generate_tts_no_text(self):
        url = reverse('generate_tts', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_generate_tts_invalid_method(self):
        url = reverse('generate_tts', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid method')

    def test_story_completed_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('story_completed', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['completed'])

        # Check that CompletedStory was created
        self.assertTrue(
            CompletedStory.objects.filter(
                user=self.user,
                story=self.story,
                language=self.language
            ).exists()
        )
    # Test story_completed view with no story
    def test_story_completed_view_no_story(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('story_completed', kwargs={'story_id': 999, 'language_id': 1})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    # Test completed_stories view
    def test_completed_stories_view(self):
        # Create a story
        CompletedStory.objects.create(
            user=self.user,
            story=self.story,
            language=self.language
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('completed_stories'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'completed_stories.html')
        self.assertEqual(len(response.context['completed_stories']), 1)

#######################################################################################################################
# JAVASCRIPT INTEGRATION TESTING SECTION
# Test JavaScript functionality by testing the backend endpoints it interacts with
#######################################################################################################################
class JavaScriptFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.language = Language.objects.create(id=1, name='English')
        self.story = Story.objects.create(id=1, title='Test Story')

    def test_story_completion_api_endpoint(self):
        # Test the API endpoint that JavaScript onStoryCompleted function calls
        self.client.login(username='testuser', password='testpass123')

        # Test the POST request that JavaScript would make
        url = reverse('story_completed', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.post(
            url,
            data=json.dumps({'completed': True}),
            content_type='application/json',
            HTTP_X_CSRFTOKEN='fake_csrf_token'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['completed'])

    def test_csrf_protection(self):
        # Test that CSRF protection works
        self.client.login(username='testuser', password='testpass123')

        # Make request without CSRF token
        url = reverse('story_completed', kwargs={'story_id': 1, 'language_id': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_tts_endpoint_for_javascript(self):
        # Test the TTS endpoint that JavaScript would call
        url = reverse('generate_tts', kwargs={'story_id': 1, 'language_id': 1})

        with patch('languatale.views.gTTS') as mock_gtts:
            mock_tts_instance = Mock()
            mock_gtts.return_value = mock_tts_instance

            def mock_write_to_fp(fp):
                fp.write(b'fake_audio_data')
            mock_tts_instance.write_to_fp = mock_write_to_fp

            response = self.client.post(url, data={'text': 'Hello from JavaScript'})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'audio/mpeg')