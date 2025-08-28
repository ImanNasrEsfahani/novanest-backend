from django.urls import path
from knox.views import LogoutView
from .views import RegisterAPI,LoginAPI
app_name= "accounts"
urlpatterns = [
    path('register',RegisterAPI.as_view(),name='register'),
    path('login',LoginAPI.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name="logout"),
    
]
