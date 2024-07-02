from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.mixins import AdminStaffUserPermissionMixin
from .serializers import NewsVideoSerializer
from .models import NewsVideo
from django.core.cache import cache
from rest_framework.parsers import MultiPartParser, FormParser

import requests
import pandas as pd
from admin_panel.models import Post,Category
from account.models import User
from django.core.files.base import ContentFile
from django.core.files import File
import os  

class PostNewsVideoViews(AdminStaffUserPermissionMixin ,APIView):

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self,request):
        serializer = NewsVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsVideoListView(APIView):
    def get(self, request):
        if cache.get("videos"):
            news_videos=cache.get("videos")
            print(news_videos)
        else:    
            news_videos = NewsVideo.objects.all()
            cache.set("videos",news_videos, timeout=60)
        serializer = NewsVideoSerializer(news_videos, many=True)
        return Response(serializer.data) 
    
class NewsVideoUpdateView(AdminStaffUserPermissionMixin, APIView):

    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        id = request.data.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            news_video = NewsVideo.objects.get(id=id)
            serializer = NewsVideoSerializer(news_video,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsVideo.DoesNotExist:
            return Response({'info': 'News Video not found'}, status=status.HTTP_404_NOT_FOUND)
        
class NewsVideoDeleteView(AdminStaffUserPermissionMixin ,APIView):

    def delete(self, request):
        id = request.data.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            news_video = NewsVideo.objects.get(id=id)
            news_video.delete()
            return Response({'info': 'News Video deleted successfully'}, status=status.HTTP_200_OK)
        except NewsVideo.DoesNotExist:
            return Response({'info': 'News Video not found'}, status=status.HTTP_404_NOT_FOUND)
       
# Route to get data and save into databases
class Test(APIView):
    def get(self, request):
        API_KEY = '034c373ed2984aecb086fbf614f3fffe'
        s='Business'
        response = requests.get(f"https://newsapi.org/v2/everything?q=AI&from=2024-06-01&sortBy=publishedAt&apiKey=bb061a9abb70445eb0a3028e54fd1d56")
        print(response)
        data = response.json()  # Simplified way to parse JSON response
        article_data = {
            'title': [article['title'] for article in data['articles']],
            'url': [article['url'] for article in data['articles']],
            'description': [article['description'] for article in data['articles']],
            'img': [article['urlToImage'] for article in data['articles']]
        }
        df = pd.DataFrame(article_data)
        print(df)
        c=Category.objects.get(id='09b07f1f-de97-471e-b909-f1a2792823ec')
        u=User.objects.get(id=1)
        # Save to database
        for index, row in df.iterrows():
            post=Post(
                title=row['title'],
                description=row['description'],
                category=c,
                author=u
            )
            filename = os.path.basename(row['img']) 
            file_content = ContentFile(requests.get(row['img']).content)
            django_file = File(file_content, name=f'{filename}.jpeg')
            print(file_content,django_file)
        # Save the file to the ImageField
            post.post_img=django_file
            post.save()

        return Response({'data': 'info'}, status=200)