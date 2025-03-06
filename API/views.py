import json
import os
from django.shortcuts import render, redirect
from django.conf import settings
import random

EXAM_SESSION_KEY = "exam_questions"

def index(request):
    return render(request, 'index.html')

def open_file(request, modulo):
    json_file = os.path.join(settings.BASE_DIR, f"data/{modulo}.json")

    if not os.path.exists(json_file):
        return render(request, 'error.html', {'message': f"No se encontraron preguntas para el módulo {modulo}."})

    with open(json_file, "r", encoding="utf-8") as file:
        questions = json.load(file)

    return questions

def quiz_view(request, modulo):
    questions = open_file(request, modulo)

    total_questions = len(questions)
    current_index = int(request.session.get(f'current_index_{modulo}', 0))
    correct_answers = int(request.session.get(f'correct_answers_{modulo}', 0))

    if current_index >= total_questions:
        request.session.pop(f'current_index_{modulo}', None)
        request.session.pop(f'correct_answers_{modulo}', None)
        return render(request, 'quiz_result.html', {'score': correct_answers, 'total': total_questions})

    current_question = questions[current_index]

    is_correct = None
    selected_answer = None
    show_feedback = False

    if request.method == 'POST':
        selected_answer = request.POST.get('answer')

        if selected_answer:
            correct_answer = current_question['answer']

            is_correct = (selected_answer == correct_answer)
            
            if is_correct:
                request.session[f'correct_answers_{modulo}'] = correct_answers + 1

            request.session[f'current_index_{modulo}'] = current_index + 1
        
            show_feedback = True
    
    return render(request, 'quiz.html', {
        'question': current_question,
        'options': current_question['options'],
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'selected_answer': selected_answer,
        'modulo': modulo.replace('_',' '),
    })

def reset_preguntas(request, modulo):
    request.session.pop(f'current_index_{modulo}', None)
    request.session.pop(f'correct_answers_{modulo}', None)
    return redirect('index')

def start_exam(request):
    all_questions = open_file(request, "Todas_las_preguntas")
    if len(all_questions) < 10:
        return render(request, "error.html", {"message": "No hay suficientes preguntas para el examen."})

    exam_questions = random.sample(all_questions, 10)
    request.session[EXAM_SESSION_KEY] = {"questions": exam_questions, "current_index": 0, "score": 0}
    
    return redirect("exam_question")


def exam_question(request):
    """
    Muestra la pregunta actual del examen y permite avanzar a la siguiente.
    """
    exam_data = request.session.get(EXAM_SESSION_KEY, {})
    questions = exam_data.get("questions", [])
    current_index = exam_data.get("current_index", 0)
    score = exam_data.get("score", 0)

    if current_index >= len(questions):
        return redirect("exam_result")

    current_question = questions[current_index]
    selected_answer = request.POST.get("answer", None)
    show_feedback = False
    is_correct = None

    if request.method == "POST":
        if selected_answer:
            correct_answer = current_question["answer"]
            is_correct = (selected_answer == correct_answer)
            if is_correct:
                exam_data["score"] += 1
            exam_data["current_index"] += 1
            request.session[EXAM_SESSION_KEY] = exam_data
            show_feedback = True

    return render(request, "exam.html", {
        "question": current_question,
        "current_index": current_index + 1,
        "total_questions": len(questions),
        "show_feedback": show_feedback,
        "is_correct": is_correct,
        "selected_answer": selected_answer,
    })

def exam_result(request):
    """
    Muestra el resultado final del examen.
    """
    exam_data = request.session.get(EXAM_SESSION_KEY, {})
    score = exam_data.get("score", 0)
    total_questions = len(exam_data.get("questions", []))

    request.session.pop(EXAM_SESSION_KEY, None)  # Eliminar datos de examen tras finalizar

    return render(request, "exam_result.html", {
        "score": score,
        "total_questions": total_questions
    })