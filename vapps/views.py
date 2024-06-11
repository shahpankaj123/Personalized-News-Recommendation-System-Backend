from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.mixins import AdminStaffUserPermissionMixin
from .serializers import NewsVideoSerializer
from .models import NewsVideo
from rest_framework.parsers import MultiPartParser, FormParser

import requests
import pandas as pd
import json
from admin_panel.models import Post,Category
from account.models import User
from django.core.files.base import ContentFile
from django.core.files import File

class PostNewsVideoViews(APIView):

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self,request):
        serializer = NewsVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsVideoListView(APIView):
    def get(self, request):
        news_videos = NewsVideo.objects.all()
        serializer = NewsVideoSerializer(news_videos, many=True)
        return Response(serializer.data) 
       
import os   
class Test(APIView):
    def get(self, request):
        API_KEY = '034c373ed2984aecb086fbf614f3fffe'
        response = requests.get(f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={API_KEY}")
        data = response.json()  # Simplified way to parse JSON response
        article_data = {
            'title': [article['title'] for article in data['articles']],
            'url': [article['url'] for article in data['articles']],
            'description': [article['description'] for article in data['articles']],
            'img': [article['urlToImage'] for article in data['articles']]
        }
        df = pd.DataFrame(article_data)
        # Save to database
        for index, row in df.iterrows():
            post=Post(
                title=row['title'],
                description=row['description'],
                category=Category.objects.get(id='be534fc5120f4da383ddc1ef789057e1'),
                author=User.objects.get(id=1)
            )
            file_content = ContentFile(requests.get(row['img']).content)
            django_file = File(file_content, name=index)
        # Save the file to the ImageField
            post.post_img.save(index, django_file, save=True)
            post.save()

        return Response({'data': 'info'}, status=200)