from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),





]
