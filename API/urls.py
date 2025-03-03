from django.urls import path
from . import views 

nameapp = 'API'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('quiz/', views.quiz_view, name='quiz'),  # Página del quiz
]
