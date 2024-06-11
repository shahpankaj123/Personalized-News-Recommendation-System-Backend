from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.mixins import AdminStaffUserPermissionMixin
from .serializers import NewsVideoSerializer
from .models import NewsVideo
from rest_framework.parsers import MultiPartParser, FormParser

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