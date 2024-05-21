from django.urls import path
from account import views as vw

urlpatterns = [
    path('user/csrf_cookie', vw.GetCSRFToken.as_view(), name='csrf_cookie'),
    path('user/register',vw.RegistrationView.as_view(),name='register'),
    path('user/activate/<id>/<token>',vw.ActivateUser.as_view(),name='activate'),
    path('user/Login',vw.LoginView.as_view(),name='login'),
    path('user/Logout',vw.LogoutVeiw.as_view(),name='logout'),
    
]