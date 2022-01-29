from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser().as_view(), name='register-user'),
    path('<int:id>/<str:verify_token>/', views.VerifyUser().as_view(), name='verify-account'),
    path('login-user/', views.LoginUser().as_view(), name='login-user')
]
