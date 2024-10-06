from django.conf import settings
from django.db import models

class Video(models.Model):
    url = models.FileField(upload_to='videos/') # Changed to filefield so u can upload videos
    title = models.CharField(max_length=255)
    description = models.TextField()
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    is_liked = models.BooleanField(default=False)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'video'