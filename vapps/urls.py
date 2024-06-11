from django.urls import path
from .views import *

urlpatterns = [
    path('create/',PostNewsVideoViews.as_view()),
    path('',NewsVideoListView.as_view()),
    path('test/',Test.as_view()),
]