from django.db import models

class Video(models.Model):
    url = models.CharField(max_length=255, null=False, default='')
    title = models.CharField(max_length=255)
    description = models.TextField()
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    is_liked = models.BooleanField(default=False)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
