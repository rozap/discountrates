# Create your views here.
from django.http import HttpResponse
from discount.decorators import json_view
from quiz.models import Quiz, Question
from validators import QuizValidator
from discount.util import get_moneys, get_overlap
import json
import numpy as np
import uuid
import math


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
            save_priority = data['save_priority'],
            net_worth = data['net_worth']
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


    questions = Question.objects.filter(quiz = quiz)

    if quiz.overlap == None:
        quiz.overlap = get_overlap(quiz)

        rates = [float(q.discount_rate) for q in questions]
        quiz.avg_rate = np.mean(rates)
        quiz.save()




    quizzes = Quiz.objects.filter(overlap__isnull = False)

    overlaps = [q.overlap for q in quizzes]
    stabilities = {i : 0 for i in range(21)}
    for o in overlaps:
        stabilities[o] = stabilities[o] + 1
    avg = np.mean(overlaps)
    stdev = np.std(overlaps)

    average_rates = [float(q.avg_rate) for q in quizzes]
    bucket_num = 20
    average_buckets = {i : 0 for i in range(bucket_num)}
    #Constrain rate between .978 and 1
    base_rate = .978
    window = float(1 - base_rate)
    inc = window/bucket_num
    for a in average_rates:
        b = math.floor((a - base_rate) / inc)
        average_buckets[b] = stabilities[b] + 1
    rate_avg = np.mean(average_rates)
    rate_stdev = np.std(average_rates)

    final_buckets = {}
    for k in average_buckets:
        nk = base_rate + (inc * int(k))
        final_buckets[nk] = average_buckets[k]
    


    return {'stability_avg' : avg, 'stability_stdev' : stdev, 'stabilities' : stabilities, 
            'averages' : final_buckets, 'avg_rate' : rate_avg, 'rate_stdev' : rate_stdev,
            'quiz' : quiz, 'questions' : list(questions)}

    