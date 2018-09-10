from rest_framework.fields import Field
from comments.writers import get_writer


class OutputField(Field):

    def to_internal_value(self, data):
        return get_writer(data)

    def validate_empty_values(self, data):
        if data is None:
            return False, get_writer()
        return False, data
