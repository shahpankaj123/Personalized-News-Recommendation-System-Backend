from rest_framework.response import Response
from account.models import *
from admin_panel.models import *
from rest_framework.views import APIView
from admin_panel.serializers import PostSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from admin_panel.serializers import CategorySerializer

class CategoryGetView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RandomPostView(APIView):
    def get(self,request):
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)
            posts = Post.objects.filter(post_date__range=[start_date, end_date])
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while fetching random posts.'}, status=status.HTTP_400_BAD_REQUEST)

class LatestPostView(APIView):
    def get(self,request):
        try:
            posts = Post.objects.order_by('-post_date')[:5]
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while fetching the latest posts.'}, status=status.HTTP_400_BAD_REQUEST)
        
class CategorywisePostView(APIView):
    def get(self, request):
        try:
            category = request.GET.get('categoryId')
            if not category:
                return Response({'error': 'Category parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)

            posts = Post.objects.filter(category__id=category, post_date__range=[start_date, end_date])
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
            posts = Post.objects.filter(title__icontains=search).order_by('-post_date')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while searching for posts.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)