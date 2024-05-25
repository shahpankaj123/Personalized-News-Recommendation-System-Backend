from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from admin_panel.serializers import UserSerializer,PostSerializer,CategorySerializer
from .models import Category,Post

class UserListView(APIView):
    #This view is for listing all users and creating a new user.
    permission_classes = [permissions.IsAdminUser]
    #It restricts access to admin users only
    def get(self, request):
        #Retrieves all User instances from the database.
        #Serializes them using UserSerializer with many=True indicating multiple objects.
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
    #it saves the new User and returns the serialized data with a 201 Created status.
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'info':'Invalid User Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    #This view is for retrieving, updating, and deleting a specific user by their primary key (id).
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        #Retrieves the user by id, then updates it with the data from the request.
        user = self.get_object(id)
        if user is None:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class CategoryView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get_object(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request,id):
        posts = self.get_object(id)
        if posts is None:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self,request,id):
        posts = self.get_object(id)
        if posts is None:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        posts.delete()
        return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)







