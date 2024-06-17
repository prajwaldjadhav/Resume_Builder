from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('profile/', views.profile, name="profile"),
    path('editor', views.editor, name="editor"),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('choose_template', views.choose_template, name='choose_template'),
]