from django.db import models

# Create your models here.
class Contact(models.Model):

    class Meta:
        db_table = 'Contact'

    name=models.CharField(max_length=100)
    phone = models.CharField(max_length=20) 
    message=models.TextField()

    def __str__(self):
        return f'{self.name}+{self.phone}'