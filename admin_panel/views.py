from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from admin_panel.serializers import UserSerializer

class UserListView(APIView):
    #This view is for listing all users and creating a new user.
    #permission_classes = [permissions.IsAdminUser]
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
    #This view is for retrieving, updating, and deleting a specific user by their primary key (pk).
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        #Retrieves the user by pk, then updates it with the data from the request.
        user = self.get_object(pk)
        if user is None:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({'info': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'info': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)






