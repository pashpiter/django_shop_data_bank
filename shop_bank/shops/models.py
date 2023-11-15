from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_time


class City(models.Model):
    city_name = models.CharField(verbose_name='Название города',
                                 max_length=30)
    
    def __str__(self):
        return f'{self.name}'


class Street(models.Model):
    street_name = models.CharField(verbose_name='Название улицы',
                                   max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             related_name='streets',
                             verbose_name='Город')
    
    def __str__(self):
        return f'{self.name}'


class Shop(models.Model):
    shop_name = models.CharField(verbose_name='Название магазина',
                                 max_length=30)
    street = models.ForeignKey(Street, on_delete=models.CASCADE,
                               related_name='shops',
                               verbose_name='Улица')
    house_number = models.PositiveIntegerField(
        verbose_name='Номер дома',
        validators=(MinValueValidator(1), MaxValueValidator(200))
    )
    time_open = models.TimeField(verbose_name='Время открытия',
                                 validators=(validate_time,))
    time_close = models.TimeField(verbose_name='Время закрытия',
                                  validators=(validate_time,))
    
    def __str__(self):
        return f'{self.name}'
