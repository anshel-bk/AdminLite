from django.db import models
from taggit.managers import TaggableManager


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    resource = models.CharField(max_length=200)
    created_at = models.DateField()
    tags = TaggableManager()

    def __str__(self):
        return self.title
