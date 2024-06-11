from django.urls import path
from .views import *

urlpatterns = [
    path('random/',RandomPostView.as_view()),
    path('latest/',LatestPostView.as_view()),
    path('categorywise/',CategorywisePostView.as_view()),
    path('search/',SearchPostView.as_view()),
    path('get_category/',CategoryGetView.as_view()),
]