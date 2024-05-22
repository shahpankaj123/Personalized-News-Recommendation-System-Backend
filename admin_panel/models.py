from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    preferences = models.JSONField(default=dict)  # Store user preferences as JSON

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    tags = models.JSONField(default=list)  # Store tags as a list of strings

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.FloatField()  # Recommendation score
    created_at = models.DateTimeField(auto_now_add=True)

