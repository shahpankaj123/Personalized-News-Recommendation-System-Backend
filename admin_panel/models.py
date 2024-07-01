from django.db import models
from account.models import User
import uuid

class Category(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return f'{self.id}+{self.name}'   

class Post(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    post_date = models.DateField(auto_now=True)
    post_time=models.TimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    post_img = models.ImageField(upload_to='post_images/')

    class Meta:
        db_table = 'Post'

    def __str__(self):
        return self.title     

