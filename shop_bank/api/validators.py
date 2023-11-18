from django.shortcuts import get_object_or_404
from shops.models import City, Street

from rest_framework.exceptions import ValidationError


def validate_input_params_city_street_open(city, street, opn):
    """Проверка города и улицы в базе, проверка занчения opn"""
    if city:
        if not City.objects.filter(name=city).exists():
            raise ValidationError({'message': f'Города {city} нет в базе'})
        else:
            city_obj = get_object_or_404(City, name=city)
        if street:
            if not Street.objects.filter(name=street, city=city_obj).exists():
                raise ValidationError(
                    {'message': f'Улицы {street} нет в городе {city}'})
    if street:
        if not Street.objects.filter(name=street).exists():
            raise ValidationError(
                {'message': f'Улицы {street} нет в базе'})
    if opn:
        if opn not in ('01'):
            raise ValidationError(
                {'message': 'Параметр "open" может быть только 0 или 1'})
