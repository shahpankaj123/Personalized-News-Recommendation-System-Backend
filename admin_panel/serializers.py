from rest_framework import serializers
from account.models import User
from .models import Category,Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin','is_active','is_staffusers','password']

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
        fields = ['id','name']

class PostSerializer(serializers.ModelSerializer):
    
    author=serializers.ReadOnlyField(source='author.username')
    category=serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Post
        fields = ['id','title', 'description', 'category','author','post_img','post_date','post_time']
    post_img = serializers.ImageField(use_url=True)    
        


