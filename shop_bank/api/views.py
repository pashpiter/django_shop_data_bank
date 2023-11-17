from datetime import datetime

from rest_framework import mixins, views, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import CitySerializer, StreetSerializer, ShopSerializer
from shops.models import City, Street, Shop


class PingView(views.APIView):
    def get(self, request):
        return Response({'app': 'django_shop_data_bank', 'version': '1.0'},
                        status=200)


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Street.objects.all()
    serializer_class = StreetSerializer

    def get_queryset(self):
        query = self.queryset.filter(city=self.kwargs['city_id'])
        if not query:
            raise ValidationError({'message': 'Нет города с таким ID'})
        return query


class ShopModelViewSet(viewsets.ModelViewSet):

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city', False)
        street = self.request.query_params.get('street', False)
        opn = int(self.request.query_params.get('open', 0))
        query = self.queryset.all()
        query = query.filter(city__name=city) if city else query
        query = query.filter(street__name=street) if street else query
        now = datetime.now().time()
        query = query.filter(
            time_open__lte=now, time_close__gt=now
        ) if opn else query
        return query

    def create(self, request, *args, **kwargs):
        """Изменение status code в случае создания нового объекта Shop"""
        response = super().create(request, *args, **kwargs)
        response.status_code = 200
        return response
