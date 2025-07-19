from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_face, name='register'),
    path('recognize/', views.recognize_face_and_hand, name='recognize'),
    path('gate-open/<str:user_name>/', views.gate_open, name='gate_open'),
]