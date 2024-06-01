from django.urls import path
from account import views as vw

urlpatterns = [
    path('user/register',vw.RegistrationView.as_view(),name='register'),
    path('user/activate/<id>/<token>',vw.ActivateUser.as_view(),name='activate'),
    path('user/login',vw.LoginView.as_view(),name='login'),
    path('user/logout',vw.LogoutView.as_view(),name='logout'),
    
]