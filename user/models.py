from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model with email as the unique identifier.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    favorite_categories = models.ManyToManyField('category.Category', through='UserCategory', related_name='users', blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    followers = models.ManyToManyField('self', through='UserFollowers', related_name='followed_by_this_user',
                                       symmetrical=False)
    following = models.ManyToManyField('self', through='UserFollowing', related_name='followers_of_this_user',
                                       symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'



class UserCategory(models.Model):
    """
    Intermediate model for user's favorite categories.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_favorite_categories'


class UserFollowers(models.Model):
    """
    Intermediate model for user's followers.
    """
    user_from = models.ForeignKey(User, related_name='following_relationships', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='follower_relationships', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_followers'


class UserFollowing(models.Model):
    """
    Intermediate model for user's following.
    """
    user_from = models.ForeignKey(User, related_name='follower_relationships_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='following_relationships_set', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_following'

class CodeSnippet(models.Model):
    """
    Model for the code snippets.
    """
    title = models.CharField(max_length=255)
    code = models.TextField()
    language = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_snippets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'code_snippet'
