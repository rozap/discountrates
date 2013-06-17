# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext



def home(request):
    return render_to_response('quiz/quiz.html', {}, RequestContext(request))

def result(request, quiz_id):
    return render_to_response('quiz/result.html', {'quiz':quiz_id}, RequestContext(request))