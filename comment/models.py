from django.conf import settings
from django.db import models


class Comment(models.Model):
    """
    Comment model to store comments on videos.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_id = models.ForeignKey('video.Video', related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    like_count = models.BigIntegerField(default=0)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'comment'
