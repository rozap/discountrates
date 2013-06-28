from django.db import models
from django.contrib.sessions.models import Session
from datetime import datetime
from discount.models import ResourceModel

# Create your models here.
class Quiz(ResourceModel):
    session = models.CharField(max_length = 512)
    expected_return = models.DecimalField(max_digits = 4, decimal_places = 2)
    expected_life = models.IntegerField(default = 60)
    net_worth = models.IntegerField(default = 0)
    create_date = models.DateTimeField(auto_now_add = True, default = datetime.now())
    overlap = models.IntegerField(default = None, null = True)


class Question(ResourceModel):
    discount_rate = models.DecimalField(max_digits = 6, decimal_places = 5)
    years = models.IntegerField()
    start_amount = models.IntegerField()
    end_amount = models.IntegerField()
    quiz = models.ForeignKey(Quiz)
    order = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add = True, default = datetime.now())
    choice = models.NullBooleanField(default = None, null = True)

    def as_resource(self):
        d = super(Question, self).as_resource()
        d['text'] = 'Would you rather take $%s now or $%s %s years from now?' % (format(int(self.start_amount), ",d"), format(int(self.end_amount), ",d"), self.years)
        return d

