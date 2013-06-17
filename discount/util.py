import math
import random
from quiz.models import Question, Quiz

# (ln(Money now)/ln(Money later))^(1/Compounding rate)
#MONEY_NOW = e^(DISCOUNT_RATE^TIME * ln(MONEY_LATER))
def get_moneys(quiz):
    discount_rate = random.uniform(.978, 1)
    time = random.randint(1, quiz.expected_life)
    money_later = random.randint(100, 8000000)
    exp = math.pow(discount_rate, time) * math.log(money_later)
    money_now = math.pow(math.e, exp)
    return money_now, money_later, time, discount_rate

def get_overlap(quiz):
    overlap = 0
    questions = Question.objects.filter(quiz = quiz)
    for question in questions:
        greater_than = [q for q in questions if (not q.choice == question.choice) and (q.discount_rate >= question.discount_rate) ]
        less_than    = [q for q in questions if (not q.choice == question.choice) and (q.discount_rate <= question.discount_rate) ]
        if len(greater_than) > 0 and len(less_than) > 0:
            overlap += 1
    return overlap
