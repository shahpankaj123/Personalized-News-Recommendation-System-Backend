from django.contrib import admin
from .models import User, Article, Recommendation

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Recommendation)
