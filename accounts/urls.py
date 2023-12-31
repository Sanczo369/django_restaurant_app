from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetpassword_validation/<uidb64>/<token>/', views.resetpassword_validation, name='resetpassword_validation'),
]