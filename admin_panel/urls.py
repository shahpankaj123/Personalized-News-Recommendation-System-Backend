from django.urls import path
from .views import (
    UserListView,UserDetailView,ArticleListView,ArticleDetailView,
    RecommendationListView,RecommendationDetailView,RecommendationAnalyticsView,
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('recommendations/', RecommendationListView.as_view(), name='recommendation-list'),
    path('recommendations/<int:pk>/', RecommendationDetailView.as_view(), name='recommendation-detail'),
    path('recommendations/analytics/', RecommendationAnalyticsView.as_view(), name='recommendation-analytics'),
]
