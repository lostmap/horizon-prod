from django.conf import settings
from django.db import models
from django.utils import timezone
from django_summernote.fields import SummernoteTextField

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = SummernoteTextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
