import json
import os
from django.shortcuts import render, redirect
from django.conf import settings

JSON_FILE = os.path.join(settings.BASE_DIR,  'data', 'questions.json')

def index(request):
    return render(request, 'index.html')

def load_questions():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def quiz_view(request):
    questions = load_questions()
    total_questions = len(questions)

    current_index = int(request.session.get('current_index', 0))
    correct_answers = int(request.session.get('correct_answers', 0))


    if current_index >= total_questions:
        request.session.flush()  # Limpiar la sesión para reiniciar el quiz
        return render(request, 'quiz_result.html', {'score': correct_answers, 'total': total_questions})

    current_question = questions[current_index]

    is_correct = None
    selected_answer = None
    error_message = None

    if request.method == 'POST':
        selected_answer = request.POST.get('answer')

        error_message = None
        if not selected_answer:
            error_message = "⚠️ Debes seleccionar una respuesta antes de continuar."
        else:
            correct_answer = current_question['answer']
            error_message = None

            is_correct = (selected_answer == correct_answer)
            if is_correct:
                request.session['correct_answers'] = correct_answers + 1

            request.session['current_index'] = current_index + 1

            
            return render(request, 'Quiz.html', {
                'question': current_question,
                'selected_answer': selected_answer,
                'is_correct': is_correct,
                'show_feedback': True,
                'error_message': error_message, 
            })
        
    
    return render(request, 'quiz.html', {
        'question': current_question,
        'error_message': error_message, 
        'show_feedback': False,
    })
