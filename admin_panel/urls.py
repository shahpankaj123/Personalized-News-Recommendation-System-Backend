from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListGetView.as_view(), name='user-list-get'),
    path('users/create/', UserListPostView.as_view(), name='user-list-post'),
    path('single_users/', UserGetView.as_view(), name='user-get'),
    path('users/update/', UserPutView.as_view(), name='user-put'),
    path('users/delete/',UserDeleteView.as_view(), name='user-delete'),
    path('categories/',CategoryView.as_view(), name='category-list'),
    path('posts/',PostGetView.as_view(), name='post-get'),
    path('posts/delete/',PostDeleteView.as_view(), name='post-delete'),
]
