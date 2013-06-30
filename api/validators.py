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

            try:
                self.data['net_worth'] = float(self.data['net_worth'])
            except ValueError:
                self.add_field_error('net_worth', 'Your net worth needs to be a number')           

            try:
                self.data['save_priority'] = float(self.data['save_priority'])
                if(self.data['save_priority'] < 1 or self.data['save_priority'] > 7):
                    self.add_field_error('save_priority', 'Your priority of saving for the future needs to be between 0 and 7')           

            except ValueError:
                self.add_field_error('save_priority', 'Your priority of saving for the future needs to be a number')           


        except KeyError:
            self.add_error('Missing fields')
