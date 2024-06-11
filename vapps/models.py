from django.db import models
from admin_panel.models import Category
import uuid
# Create your models here.
class NewsVideo(models.Model):

    class Meta:
        db_table = 'NewsVideo'

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='videos/',null=True,blank=True)
    thumbnail_url = models.URLField(null=True,blank=True)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
