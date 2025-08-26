from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/messages/', views.room_messages, name='room_messages'),
    path('<slug:slug>/messages/create/', views.create_message, name='create_message'),
]