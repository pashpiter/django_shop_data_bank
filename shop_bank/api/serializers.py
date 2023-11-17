from rest_framework import serializers

from shops.models import City, Street, Shop
from .utils import MySlugRelatedField, open_or_close


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name')
        model = City


class StreetSerializer(serializers.ModelSerializer):

    city = serializers.ReadOnlyField(source='city.name')

    class Meta:
        fields = ('name', 'city')
        model = Street


class ShopSerializer(serializers.ModelSerializer):

    city = serializers.SlugRelatedField(queryset=City.objects.all(),
                                        slug_field='name')
    street = MySlugRelatedField(slug_field='name')
    is_open = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'city', 'street', 'house_number',
                  'time_open', 'time_close', 'is_open')
        model = Shop
        read_only_fields = ('is_open',)

    def get_is_open(self, obj):
        return open_or_close(obj)

    def validate(self, attrs):
        shop_name = attrs['name']
        city = attrs['city']
        street = attrs['street']
        if Shop.objects.filter(name=shop_name,
                               city=city,
                               street=street).exists():
            raise serializers.ValidationError(
                {'message': f'Магазин с именем {shop_name} в городе '
                 f'{city.name} на улице {street.name} уже существует'})
        return attrs
