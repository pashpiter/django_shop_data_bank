from django.test import TestCase

from shops.models import Shop, City, Street


class CityModelTests(TestCase):
    """Тесты для модели City"""

    @classmethod
    def setUpTestData(cls):
        cls.city = City.objects.create(city_name='Las Venturas')
        cls.city_name_field = cls.city._meta.get_field('city_name')

    def test_verbose_name_city(self):
        real_verbose_name = getattr(self.city_name_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Название города',
                         'Проверьте verbose_name у city_name в модели City')

    def test_max_length_city(self):
        real_max_length = getattr(self.city_name_field, 'max_length')
        self.assertTrue(real_max_length,
                        'Проверьте max_length у city_name в модели City')


class StreetModelTests(TestCase):
    """"Тесты для модели Street"""

    @classmethod
    def setUpTestData(cls):
        cls.city = City.objects.create(city_name='Las Venturas')
        cls.street = Street.objects.create(street_name='Столичная улица',
                                           city=cls.city)
        cls.street_name_field = cls.street._meta.get_field('street_name')
        cls.street_city_field = cls.street._meta.get_field('city')

    def test_verbose_name_street(self):
        field_verboses = {
            'street_name': 'Название улицы',
            'city': 'Город',
        }
        street = StreetModelTests.street
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    street._meta.get_field(value).verbose_name, expected,
                    'Ошибка в verbose_name у модели Street'
                )

    def test_max_length_name_street(self):
        real_max_length = getattr(self.street_name_field, 'max_length')
        self.assertTrue(real_max_length,
                        'Проверьте max_length у street_name в модели Street')

    def test_city_on_delete_street(self):
        self.assertTrue(self.street_city_field.many_to_one)
        self.assertTrue(self.street_city_field._check_on_delete,
                        'Проверьте on_delete_mode у city '
                        'в модели Street')

    def test_city_related_name_street(self):
        self.assertTrue(self.street_city_field._related_name,
                        'Проверьте related_name у city в модели Street')


class ShopModelTests(TestCase):
    """Тесты для модели Shop"""

    @classmethod
    def setUpTestData(cls):
        """Добавление данных в БД"""
        cls.city = City.objects.create(city_name='Las Venturas')
        cls.street = Street.objects.create(street_name='Столичная улица',
                                           city=cls.city)
        cls.shop = Shop.objects.create(shop_name='Abibas',
                                       street=cls.street,
                                       house_number=123,
                                       time_open='12:00',
                                       time_close='22:00')
        cls.shop_name_field = cls.shop._meta.get_field('shop_name')
        cls.shop_street_field = cls.shop._meta.get_field('street')
        cls.shop_house_field = cls.shop._meta.get_field('house_number')
        cls.shop_time_open_field = cls.shop._meta.get_field('time_open')
        cls.shop_time_close_field = cls.shop._meta.get_field('time_close')

    def test_verbose_names_shop(self):
        field_verboses = {
            'shop_name': 'Название магазина',
            'street': 'Улица',
            'house_number': 'Номер дома',
            'time_open': 'Время открытия',
            'time_close': 'Время закрытия',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(self.shop._meta.get_field(value).verbose_name,
                                 expected,
                                 f'Ошибка в verbose_name у {value} в '
                                 'модели Shop')

    def test_max_length_name_shop(self):
        real_max_length = getattr(self.shop_name_field, 'max_length')
        self.assertTrue(real_max_length,
                        'Проверьте max_length у shop_name в модели Shop')

    def test_street_on_delete_shop(self):
        self.assertTrue(self.shop_street_field._check_on_delete,
                        'Проверьте on_delete_mode у street '
                        'в модели Shop')

    def test_street_related_name_shop(self):
        self.assertTrue(self.shop_street_field._related_name,
                        'Проверьте related_name у street в модели Shop')

    def test_house_number_validators_shop(self):
        real_validators_value = getattr(self.shop_house_field, 'validators')
        self.assertTrue(real_validators_value,
                        'Проверьте validators у house_number в модели Shop')

    def test_time_open_validators_shop(self):
        real_validators_value = getattr(self.shop_time_open_field,
                                        'validators')
        self.assertTrue(real_validators_value,
                        'Проверьте validators у time_open в модели Shop')

    def test_time_close_validators_shop(self):
        real_validators_value = getattr(self.shop_time_close_field,
                                        'validators')
        self.assertTrue(real_validators_value,
                        'Проверьте validators у time_close в модели Shop')
