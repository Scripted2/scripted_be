from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    favorite_categories = models.ManyToManyField('Category', related_name='users', blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    followers = models.ManyToManyField('self', related_name='followed_by_this_user', symmetrical=False)
    following = models.ManyToManyField('self', related_name='followers_of_this_user', symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CodeSnippet(models.Model):
    title = models.CharField(max_length=255)
    code = models.TextField()
    language = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_snippets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
