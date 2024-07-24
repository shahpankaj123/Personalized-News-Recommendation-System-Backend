from rest_framework.response import Response
from account.models import *
from admin_panel.models import *
from rest_framework.views import APIView
from admin_panel.serializers import PostSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from django.core.cache import cache
from admin_panel.serializers import CategorySerializer
from django.shortcuts import render, get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import pickle

category_mapping = {
        '000':'SPORTS',
        '001':'TECH',
        '010':'POLITICS',
        '011':'SCIENCE',
        '100':'ENTERTAINMENT',
        '101':'RELIGION',
        '110':'EDUCATION',
        '111':'ENVIRONMENT',       
    }

def get_similar_posts(post_id,cat_id ,num_recommendations=60):
    posts = Post.objects.filter(category__id=cat_id)
    post_contents = [post.title for post in posts]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(post_contents)
    
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    post_indices = {post.id: index for index, post in enumerate(posts)}
    idx = post_indices[post_id]

    similarity_scores = list(enumerate(cosine_similarities[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similar_post_indices = [i[0] for i in similarity_scores[1:num_recommendations + 1]]
    
    similar_posts = [posts[i] for i in similar_post_indices]
    rest_post=Post.objects.exclude(category__id=cat_id)[0:20]
    post=similar_posts+list(rest_post)
    return post

def Predict(title):
    try:
        model = pickle.load(open('model/finalized_model.sav', 'rb'))
        prediction = model.predict([title])
        print(prediction)
        key=category_mapping.get(prediction[0])
        print(key)
        cat=Category.objects.get(name=key)
        print(cat)
        post_id=Post.objects.filter(category__id=cat.id).first()
        print(post_id,cat)   
        posts=get_similar_posts(post_id.id,cat.id, num_recommendations=35)
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    except Exception as e:
        print(f"An error occurred during prediction: {str(e)}")
        return None
    
def get_news():
    try:
        posts = Post.objects.all().order_by('-post_date')
        serializer = PostSerializer(posts, many=True)
        posts = serializer.data        
        return Response(posts, status=status.HTTP_200_OK)         
    except Exception as e:
        return Response({'error': f'An error occurred while fetching random posts: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        
class RandomPostView(APIView):
    def get(self, request): 
        print(cache.get("email"))  
        if cache.get("email"):
            if cache.get('recommend_post'):
                recommended_post_title = cache.get('recommend_post')
                prediction = Predict(recommended_post_title)
                if prediction:
                    return Response(prediction, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Prediction failed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return get_news()
        else:
            return get_news()     



class CategoryGetView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LatestPostView(APIView):
    def get(self,request):
        try:
            if cache.get("latest-posts"):
                posts=cache.get("latest-posts")
            else:    
                posts = Post.objects.order_by('-post_date')[:8]
                cache.set("latest-posts",posts, timeout=60)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while fetching the latest posts.'}, status=status.HTTP_400_BAD_REQUEST)
        
class CategorywisePostView(APIView):
    def get(self, request):
        try:
            category = request.GET.get('categoryId')
            if not category:
                return Response({'error': 'Category parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)

            if cache.get(f"category-posts{category}"):
                posts=cache.get(f"category-posts{category}")
            else:    
                posts = Post.objects.filter(category__id=category).order_by('-post_date')
                cache.set(f"category-posts{category}",posts, timeout=60)

            #posts = Post.objects.filter(category__id=category, post_date__range=[start_date, end_date])
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except:
            return Response({'error': 'An error occurred while fetching category-wise posts.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SearchPostView(APIView):
    def get(self, request):
        try:
            search = request.GET.get('search')
            if not search:
                return Response({'error': 'Search parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            posts = Post.objects.filter(title__icontains=search).order_by('-post_date')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while searching for posts.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SinglePostView(APIView):
    def get(self, request):
        try:
            id = request.GET.get('postId')
            if not id:
                return Response({'error': 'postId parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            posts = Post.objects.get(id=id)
            serializer = PostSerializer(posts)
            cache.delete('recommend_post')
            cache.set("recommend_post",posts.description,timeout=86400)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred while fetching category-wise posts.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

              