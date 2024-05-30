from django.shortcuts import render
from account.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from account import serializers as sr
from rest_framework.authtoken.models import Token
from django.conf import settings
from account.utils import send_activation_email,send_reset_password_email

def custom_404(request, exception):
    return render(request, 'accounts/404.html', status=404)

class RegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=sr.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_url = 'http://127.0.0.1:8000/api/account/user/activate/'+ uid + '/' + token
            send_activation_email(user.email, activation_url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

  
class ActivateUser(APIView):
    permission_classes=[AllowAny]
    def get(self,request,id,token):
        id=force_str(urlsafe_base64_decode(id))
        print(id)
        if not id or not token:
            return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id=id)
        if default_token_generator.check_token(user, token):
            if user.is_active:
                return Response({'detail': 'Account is already activated.'}, status=status.HTTP_200_OK)
 
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)      


class LoginView(APIView):
    def post(self,request):
            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'email':email,'token':token.key},status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Account not Activated.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': 'Invalid Username or Password.'}, status=status.HTTP_400_BAD_REQUEST)   
    
class LogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK) 
    