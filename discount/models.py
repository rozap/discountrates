from django.db import models

# Create your models here.
class ResourceModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        self.extras = {}
        super(ResourceModel, self).__init__(*args, **kwargs)

    def as_resource(self):
        d = {f.name: f.value_from_object(self) for f in self._meta.local_fields}
        d.update(self.extras)
        return d

    def push_field(self, name, value):
        self.extras[name] = value
        return self
