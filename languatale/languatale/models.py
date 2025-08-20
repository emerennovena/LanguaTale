from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Story(models.Model):
    title = models.CharField(max_length=200)
    author = models. CharField(max_length=100)
    available_languages = models.ManyToManyField(Language, related_name='stories')

    ink_json_content = JSONField(
        help_text = "The compiled JSON story content of the Ink story exported from Inky.",
        blank = True,
        null = True
    )
    def __str__(self):
        return self.title

class CompletedStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_stories')
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story', 'language')

    def __str__(self):
        return f"{self.user.username} completed {self.story.title} in {self.language.name}"

