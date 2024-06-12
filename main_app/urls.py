from django.urls import path
from .views import *

urlpatterns = [
    path('get-random-post/',RandomPostView.as_view()),
    path('get-latest-post/',LatestPostView.as_view()),
    path('get-categorywise-post/',CategorywisePostView.as_view()),
    path('search-post/',SearchPostView.as_view()),
    path('get_category/',CategoryGetView.as_view()),
]