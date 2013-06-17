from discount.validators import Validator

class QuizValidator(Validator):

    def __init__(self, data):
        self.data = data
        super(QuizValidator, self).__init__()

    def do_validate(self):
        try:
            
            try:
                self.data['expected_return'] = float(self.data['expected_return'])
            except ValueError:
                self.add_field_error('expected_return', 'Your expected annual return needs to be a number')

            try:
                self.data['expected_life'] = float(self.data['expected_life'])
            except ValueError:
                self.add_field_error('expected_life', 'Your expected remaining years needs to be a number')           


        except KeyError:
            self.add_error('Missing fields')
