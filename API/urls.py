from django.urls import path
from . import views 

nameapp = 'API'

urlpatterns = [
    path('', views.index, name='index'),  
    path('quiz/<str:modulo>/', views.quiz_view, name='quiz'),  
    path('quiz/reset/<str:modulo>/', views.reset_preguntas, name='reset_quiz'),
]
