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
            raise ValidationError({'message': 'Нет города с таким ID'},
                                  code=400)
        return query


class ShopModelViewSet(viewsets.ModelViewSet):

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
