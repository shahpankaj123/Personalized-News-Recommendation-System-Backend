from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from admin_panel.serializers import UserSerializer,PostSerializer,CategorySerializer
from .models import Category,Post

class UserListGetView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserListPostView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'info': 'Invalid User Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserGetView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserPutView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
class CategoryView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class PostGetView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
class PostDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)






