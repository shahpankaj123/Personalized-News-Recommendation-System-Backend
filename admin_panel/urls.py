from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListGetView.as_view(), name='user-list-get'),
    path('users/new/', UserListPostView.as_view(), name='user-list-post'),
    path('users/<int:id>/', UserGetView.as_view(), name='user-get'),
    path('users/<int:id>/update/', UserPutView.as_view(), name='user-put'),
    path('users/<int:id>/delete/',UserDeleteView.as_view(), name='user-delete'),
    path('categories/',CategoryView.as_view(), name='category-list'),
    path('posts/<int:id>/',PostGetView.as_view(), name='post-get'),
    path('posts/<int:id>/delete/',PostDeleteView.as_view(), name='post-delete'),
]
