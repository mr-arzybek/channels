from django.urls import path

from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),

    path('choice/', views.choice, name='choice'),
    path('room/<int:pk>/', views.room, name='room'),
    path('', views.index, name='index'),
]
