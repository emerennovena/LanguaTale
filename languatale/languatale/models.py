from django.db import models
from django.db.models import JSONField

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