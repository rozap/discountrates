import re

class Validator(object):

    def __init__(self):
        self.errors = {}

    def add_field_error(self, field, error):
        self.errors[field] = error

    def add_error(self, error):
        if not self.errors.get('non_field_errors', False):
            self.errors['non_field_errors'] = []
        self.errors['non_field_errors'].append(error)

    def get_errors(self):
        return {'errors' : self.errors}

    def validate(self):
        self.do_validate()
        if len(self.errors.keys()) > 0:
            return False, self.get_errors()
        return True, self.data


    def validate_link(self, link):
        return len(link) > 1 and re.search('(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', link)

