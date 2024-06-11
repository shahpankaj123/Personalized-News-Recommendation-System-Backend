from rest_framework.response import Response
from account.models import *
from admin_panel.models import *
from rest_framework.views import APIView
from admin_panel.serializers import PostSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework import status

class RandomPostView(APIView):
    def get(self,request):
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)
            posts = Post.objects.filter(date__range=[start_date, end_date])
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while fetching random posts.'}, status=status.HTTP_400_BAD_REQUEST)

class LatestPostView(APIView):
    def get(self,request):
        try:
            posts = Post.objects.all().order_by('-date')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while fetching the latest posts.'}, status=status.HTTP_400_BAD_REQUEST)
        
class CategorywisePostView(APIView):
    def get(self, request):
        try:
            category = request.GET.get('category')
            if not category:
                return Response({'error': 'Category parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate the start date (3 days ago from now)
            end_date = timezone.now()
            start_date = end_date - timedelta(days=3)

            # Filter posts by category and date range
            posts = Post.objects.filter(category=category, date__range=[start_date, end_date])
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except:
            return Response({'error': 'An error occurred while fetching category-wise posts.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SearchPostView(APIView):
    def get(self, request):
        try:
            search = request.GET.get('search')
            if not search:
                return Response({'error': 'Search parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            # Calculate the date range (last 3 to 4 days)
            end_date = timezone.now()
            start_date = end_date - timedelta(days=4)
            # Filter posts by search query and date range
            # This assumes you are searching in the title or content of the posts
            posts = Post.objects.filter(date__range=[start_date, end_date]).filter(title__icontains=search).order_by('-date')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while searching for posts.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)