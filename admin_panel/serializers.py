from rest_framework import serializers
from account.models import User
from .models import Category,Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'is_staff']

    def create(self, validated_data):
        #handles creating a new User instance, including proper password handling (hashing) before saving the instance to the database.
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'category', 'post_date', 'post_time', 'author', 'post_img']
        read_only_fields = ['post_date', 'post_time']
        


