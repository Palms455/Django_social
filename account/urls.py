from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit')
]
'''
вместо прописывания стандартных путей можно ввести 
path('', include('django.contrib.auth.urls')
'''