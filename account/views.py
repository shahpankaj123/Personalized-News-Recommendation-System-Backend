from django.shortcuts import render

# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer

class RegisterView(APIView):
    """The status codes are important for communicating 
    the result of an API request to the client in a standardized manner.
    """

    """
    Here, status.HTTP_400_BAD_REQUEST is used to indicate that the request is missing required fields 
    or that the email already exists, while status.
    HTTP_201_CREATED indicates that a new user has been successfully created.
    """
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if all required fields are provided
        if username is None or email is None or password is None:
            return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user with username, email, and password
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate the user using email as the username
        user = authenticate(username=email, password=password)
        
        # Check if authentication was successful
        if user is not None:
            # Generate refresh and access tokens for the authenticated user
            """RefreshToken.for_user(user) creates a refresh token for the authenticated user, 
                and refresh.access_token generates an associated access token. 
                These tokens are then sent back to the client in the response.
            """
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
