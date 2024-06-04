from django.shortcuts import render
from django.http import HttpResponseRedirect
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
import random

def custom_404(request, exception):
    return render(request, 'accounts/404.html', status=404)

class UserRegistrationView(APIView):
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

  
class UserActivateUser(APIView):
    permission_classes=[AllowAny]
    def get(self,request,id,token):
        id=force_str(urlsafe_base64_decode(id))
        print(id)
        if not id or not token:
            return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id=id)
        if default_token_generator.check_token(user, token):
            if user.is_active:
                return HttpResponseRedirect('http://localhost:5173/valid-error') 
            user.is_active = True
            user.save()
            return HttpResponseRedirect('http://localhost:5173/verify-email')
        else:
            return HttpResponseRedirect('http://localhost:5173/valid-error')     


class UserLoginView(APIView):
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
    
class UserLogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK) 
    
class UserSendOTPViews(APIView):
    def post(self,request):
        email = request.data.get('email')
        if email is None:
            return Response({'message':'Invalid email'},status=status.HTTP_404_NOT_FOUND)
            
        user_obj=User.objects.get(email=email)
        print(user_obj)
        if user_obj is not None:
            rand_number=int(random.randint(1,1000))
            print(rand_number)
            user_obj.otp=rand_number
            user_obj.save()
            send_reset_password_email(user_obj.email,rand_number)
            return Response({'message':'Please check your mail for OTP'},status=status.HTTP_202_ACCEPTED)   
        return Response({'message':'Invalid mail'},status=status.HTTP_404_NOT_FOUND)

class UserVerifyOTPViews(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp=int(request.data.get('otp'))
        print(email,otp)
        if email is None or email == 'undefined' or email == '' or email == 'null':
            return Response({'message': 'email is Required'}, status=status.HTTP_404_NOT_FOUND)
        
        if otp is None or otp == 'undefined' or otp == '' or otp == 'null':
            return Response({'message': 'otp is Required'}, status=status.HTTP_404_NOT_FOUND)
        
        user_obj=User.objects.get(email=email)

        if user_obj is not None:
            if user_obj.otp == otp:
                user_obj.otp=10000
                user_obj.save()
                return Response({'message':'OTP Verified Sucessfully'},status=status.HTTP_200_OK)
            return Response({'message':'Invalid OTP'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Error'},status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    def post(self,request):
        email=request.data.get('email')
        passsword=request.data.get('password')
        password1=request.data.get('password1')

        if email is None or email == 'undefined' or email == '' or email == 'null':
            return Response({'message': 'email is Required'}, status=status.HTTP_404_NOT_FOUND)
        
        if passsword is None and password1 is None:
            return Response({'message': 'password is Required'}, status=status.HTTP_404_NOT_FOUND)
        
        if passsword != password1:
            return Response({'message':'Password and Confirm Password donot Match'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user_obj=User.objects.get(email=email)
        if user_obj is not None:
            if user_obj.otp==10000:
                user_obj.set_password(passsword)
                user_obj.otp=0
                user_obj.save()
                return Response({'message':'Password Changed Sucessfully'},status=status.HTTP_200_OK)
            return Response({'message':'Invalid OTP'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Error'},status=status.HTTP_400_BAD_REQUEST)



            
                
