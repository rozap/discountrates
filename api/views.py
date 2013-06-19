# Create your views here.
from django.http import HttpResponse
from discount.decorators import json_view
from quiz.models import Quiz, Question
from validators import QuizValidator
from discount.util import get_moneys, get_overlap
import json
import numpy as np
import uuid


@json_view
def quiz(request):
    if request.method == 'POST':
        session = str(uuid.uuid4())
        validator = QuizValidator(json.loads(request.body))
        valid, data = validator.validate()

        if not valid:
            return (data, 400)
        quiz = Quiz(
            session = session, 
            expected_return = data['expected_return'],
            expected_life = data['expected_life'],
            )
        quiz.save()
        return quiz
    return { 'hi' : ':)'}



@json_view
def questions(request, quiz_id):
    try: 
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        return ({'error' : 'Not found'}, 404)
    if request.method == 'GET':
        start_amount, end_amount, years, discount_rate = get_moneys(quiz)
        questions = Question.objects.filter(quiz = quiz).order_by('-order')
        if questions.exists():
            order = questions[0].order+1
        else:
            order = 0
        q = Question(
            years = years,
            start_amount = start_amount,
            end_amount = end_amount, 
            quiz = quiz, 
            discount_rate = discount_rate, 
            order = order
            )
        q.save()
    return q

@json_view
def question(request, quiz_id, question_id):
    data = json.loads(request.body)
    try: 
        question = Question.objects.filter(quiz__id = quiz_id).filter(quiz__session = data['session']).get(id = question_id)
    except Question.DoesNotExist:
        return ({'error' : 'Not found'}, 404)

    if request.method == 'PUT':
        question.choice = data['choice']
        question.save()
    return question


@json_view
def result(request, quiz_id):
    try: 
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        return ({'error' : 'Not found'}, 404)

    if quiz.overlap == None:
        quiz.overlap = get_overlap(quiz)
        quiz.save()

    questions = Question.objects.filter(quiz = quiz)


    quizzes = Quiz.objects.filter(overlap__isnull = False)
    overlaps = [q.overlap for q in quizzes]
    stabilities = {i : 0 for i in range(21)}
    for o in overlaps:
        stabilities[o] = stabilities[o] + 1
    avg = np.mean(overlaps)
    stdev = np.std(overlaps)
    return {'avg' : avg, 'std' : stdev, 'stabilities' : stabilities, 'quiz' : quiz, 'questions' : list(questions)}

    