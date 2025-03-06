from django.urls import path
from . import views 

nameapp = 'API'

urlpatterns = [
    path('', views.index, name='index'),  
    path('quiz/<str:modulo>/', views.quiz_view, name='quiz'),  
    path('quiz/reset/<str:modulo>/', views.reset_preguntas, name='reset_quiz'),
    path("modo-examen/", views.start_exam, name="start_exam"),
    path("modo-examen/pregunta/", views.exam_question, name="exam_question"),
    path("modo-examen/resultado/", views.exam_result, name="exam_result"),
]
