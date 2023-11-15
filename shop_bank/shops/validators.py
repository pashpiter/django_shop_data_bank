from datetime import datetime

from django.core.exceptions import ValidationError


def validate_time(value):
    min_value = datetime.strptime('00:00', '%H:%M').time()
    max_value = datetime.strptime('23:59', '%H:%M').time()
    if not min_value <= value <= max_value:
        raise ValidationError('Проверьте вводимое время')
