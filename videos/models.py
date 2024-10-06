from django.conf import settings
from django.db import models


class Video(models.Model):
    """
    Video model to store video details.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    is_liked = models.BooleanField(default=False)
    duration = models.FloatField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'video'
