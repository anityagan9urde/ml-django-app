from django.urls import path, re_path
from rest_framework import routers

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('loans/', views.loans, name='loans'),

    path('create_loan/<str:pk>/', views.createLoan, name="create_loan"),
    path('update_loan/<str:pk>/', views.updateInfo, name="update_loan"),
    path('delete_loan/<str:pk>/', views.deleteLoan, name="delete_loan"),

]