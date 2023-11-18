from rest_framework import mixins, views, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import CitySerializer, StreetSerializer, ShopSerializer
from .utils import open_or_close_query_filter
from .validators import validate_input_params_city_street_open
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
        opn = self.request.query_params.get('open', None)
        validate_input_params_city_street_open(city, street, opn)
        query = self.queryset.all()
        query = query.filter(city__name=city) if city else query
        query = query.filter(street__name=street) if street else query
        query = open_or_close_query_filter(
            query, opn) if opn is not None else query
        return query

    def create(self, request, *args, **kwargs):
        """Изменение status code в случае создания нового объекта Shop"""
        response = super().create(request, *args, **kwargs)
        response.status_code = 200
        return response
