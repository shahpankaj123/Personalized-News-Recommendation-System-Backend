from django.urls import path
from .views import *

urlpatterns = [
    #For Users
    path('users/all/', UserListGetView.as_view(), name='user-list-get'),
    path('users/create/', UserPostView.as_view(), name='user-post'),
    path('users/', UserGetView.as_view(), name='user-get'),
    path('users/update/', UserPutView.as_view(), name='user-put'),
    path('users/delete/',UserDeleteView.as_view(), name='user-delete'),
    #For Categories
    path('category/',CategoryGetView.as_view(), name='category-list'),
    path('category/create/',CategoryPostView.as_view(), name='category-post'),
    path('category/update/',CategoryPutView.as_view(), name='category-put'),
    path('category/delete/',CategoryDeleteView.as_view(), name='category-delete'),

    #For Posts
    path('posts/',PostGetView.as_view(), name='post-get'),
    path('posts/create/',PostPostView.as_view(), name='post-post'),
    path('posts/update/',PostPutView.as_view(), name='post-put'),
    path('posts/delete/',PostDeleteView.as_view(), name='post-delete'),

    #for Contact
    path('contact/',ContactViewApi.as_view()),
]
