from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    password1=serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username','email','password','password1']

    def validate(self, attrs):
        password=attrs.get('password')
        password1=attrs.get('password1')

        if password!=password1:
            raise serializers.ValidationError("Password and Conform Password donot Match.")   
        
        return attrs
    
    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
          raise serializers.ValidationError('User with this Email already exists.')
        return data
    
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.is_active=False
        user.save()
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]    
