from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_face, name='register'),
    path('recognize/', views.recognize_face, name='recognize'),
]