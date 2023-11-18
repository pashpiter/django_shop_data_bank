from datetime import datetime, time

from rest_framework import serializers
from django.db.models import Q, F, QuerySet

from shops.models import Street, Shop


class MySlugRelatedField(serializers.SlugRelatedField):

    def get_queryset(self):
        city = self.context['request'].data.get('city')
        street = self.context['request'].data.get('street')
        query = Street.objects.filter(city__name=city)
        if not query:
            raise serializers.ValidationError(
                {'message': 'В базе нет такого города'})
        if not query.filter(name=street).exists():
            raise serializers.ValidationError(
                {'message': f'В городе {city} нет улицы {street}'})
        return query


def now_time() -> time:
    """Возвращает время в данный момент"""
    return datetime.now().time()


def open_or_close(obj: Shop) -> bool:
    """Закрыт или открыт магазин"""
    now = now_time()
    if obj.time_open > obj.time_close:
        return (obj.time_close < now and obj.time_open <= now
                ) or (obj.time_close > now and obj.time_open >= now)
    return obj.time_open <= now < obj.time_close


def open_or_close_query_filter(query: QuerySet, opn: str) -> QuerySet:
    """Фильтрация queryset по параметру открыт или закрыт в
       зависимости от времени"""
    now = now_time()
    if opn != '0':
        list_1 = query.filter(
            Q(time_open__lte=F('time_close')),
            Q(time_open__lte=now),
            time_close__gt=now)
        list_2 = query.filter(
            Q(time_open__gt=F('time_close')),
            (Q(time_open__gte=now) & Q(time_close__gt=now) |
             Q(time_open__lte=now) & Q(time_close__lt=now)))
    else:
        list_1 = query.filter(
            Q(time_open__lte=F('time_close')),
            (Q(time_open__lt=now) & Q(time_close__lte=now) |
             Q(time_open__gt=now) & Q(time_close__gte=now)))
        list_2 = query.filter(
            Q(time_open__gte=F('time_close')),
            Q(time_open__gte=now),
            time_close__lte=now)
    concat_list = list_1 | list_2
    concat_list = concat_list.order_by('id')
    return concat_list
