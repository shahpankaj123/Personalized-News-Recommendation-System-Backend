from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from admin_panel.serializers import UserSerializer,PostSerializer,CategorySerializer
from .models import Category,Post
from account.mixins import AdminUserPermissionMixin,AdminStaffUserPermissionMixin

#Handles retrieving a list of all users.
class UserListGetView(AdminStaffUserPermissionMixin,APIView):
    def get(self, request):
        print(request.user)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Handles the creation of a new user.
class UserPostView(AdminStaffUserPermissionMixin,APIView):
    def post(self, request):
        """
        It takes user data from the request, validates and saves it if valid, 
        and returns the serialized user data. 
        If invalid, it returns an error message.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'info': 'Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieves details of a specific user based on the provided ID
class UserGetView(AdminStaffUserPermissionMixin,APIView):
    def get(self, request):
        #It fetches the user by ID, serializes the user data, and returns it. 
        id = request.GET.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
#Updates details of a specific user based on the provided ID
class UserPutView(AdminStaffUserPermissionMixin,APIView):
    def put(self, request):
        #It fetches the user by ID, validates and updates the user data if valid, and returns the updated data
        id = request.data.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
#Deletes a specific user based on the provided ID
class UserDeleteView(AdminStaffUserPermissionMixin,APIView):
    def delete(self, request):
        id = request.data.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#Retrieves a list of all categories 
class CategoryGetView(AdminStaffUserPermissionMixin,APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryPostView(AdminStaffUserPermissionMixin,APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'info': 'Created Successfully'} ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteView(AdminStaffUserPermissionMixin,APIView):
    def delete(self, request):
        id = request.GET.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'info': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

class CategoryPutView(AdminStaffUserPermissionMixin,APIView):
    def put(self, request):

        id = request.data.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'info': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
#Retrieves details of a specific post based on the provided ID
class PostGetView(AdminStaffUserPermissionMixin,APIView):
    def get(self, request):
        id = request.GET.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
#Deletes a specific post based on the provided ID
class PostDeleteView(AdminStaffUserPermissionMixin,APIView):
    def delete(self, request):
        id = request.GET.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=id)
            post.delete()
            return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PostPutView(AdminStaffUserPermissionMixin,APIView):
    def put(self, request):
        id = request.data.get('id')
        if id is None:
            return Response({'info': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'info': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PostPostView(AdminStaffUserPermissionMixin,APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'info': 'Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)