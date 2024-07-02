from django.urls import path
from .views import PostNewsVideoViews,NewsVideoListView,NewsVideoUpdateView,NewsVideoDeleteView,Test

urlpatterns = [
    path('create/',PostNewsVideoViews.as_view()),
    path('',NewsVideoListView.as_view()),
    path('update/',NewsVideoUpdateView.as_view()),
    path('delete/',NewsVideoDeleteView.as_view()),
    path('test/',Test.as_view()),
]