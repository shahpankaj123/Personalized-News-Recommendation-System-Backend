from rest_framework import serializers
from .models import NewsVideo

class NewsVideoSerializer(serializers.ModelSerializer):
        class Meta:
            model = NewsVideo
            fields = '__all__'