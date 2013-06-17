from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('api.views',
    # Examples:
    url(r'^quiz$', 'quiz', name='quiz'),
    url(r'^quiz/(?P<quiz_id>[\d]+)/questions$', 'questions', name='questions'),
    url(r'^quiz/(?P<quiz_id>[\d]+)/questions/(?P<question_id>[\d]+)$', 'question', name='questions'),
    url(r'^quiz/(?P<quiz_id>[\d]+)/result$', 'result', name='result'),
)
