from django.conf import settings
from django.db import models

from videos.name import PathAndName


class Video(models.Model):
    """
    Video model to store video details.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to=PathAndName('videos/'))
    file_hash = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    description = models.TextField()
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_videos', blank=True)
    duration = models.FloatField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'video'
