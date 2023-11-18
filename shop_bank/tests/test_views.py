from datetime import datetime
from unittest.mock import patch
import random
import string

from django.test import TestCase, Client
from rest_framework.response import Response

from shops.models import City, Street, Shop


class ShopViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """Создание Cities, Streets и Shops"""
        cls.los_santos = City.objects.create(name='Los Santos')
        cls.las_venturas = City.objects.create(name='Las Venturas')
        cls.san_vierro = City.objects.create(name='San Fierro')
        # Улица в Los Santos
        cls.street_in_los_santos = Street.objects.create(
            name='Main St',
            city=cls.los_santos)
        # Улица в Las Venturas
        cls.street_in_las_venturas = Street.objects.create(
            name='Main St',
            city=cls.las_venturas)
        # Вторая улица в Las Venturas
        cls.second_street_in_las_venturas = Street.objects.create(
            name='West St',
            city=cls.las_venturas)
        # Shop на West st в Las Venturas (1)
        cls.shop_on_west_st_in_las_venturas = Shop.objects.create(
            name='West_Las', city=cls.las_venturas,
            street=cls.second_street_in_las_venturas, house_number=33,
            time_open='9:00', time_close='21:00')
        # Shop на Main st в Las Venturas (2)
        cls.shop_on_main_st_in_las_venturas = Shop.objects.create(
            name='Main_Las', city=cls.las_venturas,
            street=cls.street_in_las_venturas, house_number=1,
            time_open='21:00', time_close='9:00')
        # Shop_2 на Main st в Las Venturas (3)
        cls.shop_on_main_st_in_las_venturas = Shop.objects.create(
            name='Main_2_Las', city=cls.las_venturas,
            street=cls.street_in_las_venturas, house_number=2,
            time_open='14:00', time_close='00:00')
        # Shop_3 на Main st в Las Venturas (4)
        cls.shop_on_main_st_in_las_venturas = Shop.objects.create(
            name='Main_3_Las', city=cls.las_venturas,
            street=cls.street_in_las_venturas, house_number=3,
            time_open='11:00', time_close='15:00')
        # Shop на Main st в Los Santos (5)
        cls.shop_on_main_st_in_los_santos = Shop.objects.create(
            name='Main_Los', city=cls.los_santos,
            street=cls.street_in_los_santos, house_number=66,
            time_open='10:00', time_close='19:00')

    def setUp(self) -> None:
        """Добавление клиента"""
        self.client = Client()

    def test_ping(self):
        """Проверка доступности сервера"""
        response: Response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'app': 'django_shop_data_bank',
                         'version': '1.0'})

    def test_get_cities(self):
        """Проверка получения списка городов"""
        respose: Response = self.client.get('/city/')
        expected_data = [self.los_santos.name, self.las_venturas.name,
                         self.san_vierro.name]
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(len(expected_data), len(respose.data))
        for city in respose.data:
            self.assertIn(city['name'], expected_data)

    def test_get_streets(self):
        """Проверка получения списка улиц в городе по city_id"""
        response: Response = self.client.get('/city/1/street/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        response: Response = self.client.get('/city/2/street/')
        self.assertEqual(len(response.data), 2)

    def test_get_streets_invalid_city_id(self):
        """Проверка ошибки при невалидном city_id"""
        response: Response = self.client.get('/city/12/street/')
        self.assertEqual(response.status_code, 400)

    def test_get_shop_without_params(self):
        """Проверка получения списка магазинов без параметров в GET запросе"""
        response: Response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    @patch('api.utils.now_time')
    def test_get_shop_with_valid_params_all(self, now_time_mock):
        """Проверка получения списка магазинов со всеми параметрами
           в GET запросе"""
        now_time_mock.return_value = datetime.strptime('15:00', '%H:%M').time()
        params = '?street=Main St&open=1&city=Las Venturas'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        params = '?street=Main St&open=0&city=Las Venturas'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 2)

        now_time_mock.return_value = datetime.strptime('00:00', '%H:%M').time()
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 2)

        params = '?street=Main St&open=1&city=Las Venturas'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 1)

    def test_get_shop_with_valid_params_street(self):
        """Проверка фильтрации по названию улицы"""
        params = '?street=Main St'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        params = '?street=West St'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 1)

    def test_get_shop_with_valid_params_city(self):
        """Проверка фильтрации по названию города"""
        params = '?city=Los Santos'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        params = '?city=Las Venturas'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 4)
        params = '?city=San Fierro'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 0)

    @patch('api.utils.now_time')
    def test_get_shop_with_valid_params_open(self, now_time_mock):
        """Проверка фильтрации по параметру open"""
        params = '?open=1'
        now_time_mock.return_value = datetime.strptime('15:00', '%H:%M').time()
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        params = '?open=0'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 2)

    @patch('api.utils.now_time')
    def test_get_shop_with_valid_params_street_open(self, now_time_mock):
        """Проверка фильтрации по параметрам street & open"""
        params = '?street=Main St&open=1'
        now_time_mock.return_value = datetime.strptime('15:00', '%H:%M').time()
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        params = '?street=Main St&open=0'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(len(response.data), 2)

    def test_get_shop_with_valid_params_city_street(self):
        """Проверка фильтрации по параметрам street & city"""
        params = '?street=Main St&city=Las Venturas'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_shop_with_invalid_city(self):
        """Проверка фильтрации по несуществующему городу"""
        params = '?city=San Andreas'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 400)

    def test_get_shop_with_invalid_street(self):
        """Проверка фильтрации по несуществующей улице"""
        params = '?street=Blabla St'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 400)

    def test_get_shop_with_invalid_open(self):
        """Проверка фильтрации по невалидному значению open"""
        params = '?open=11'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 400)
        params = '?open=-1'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 400)

    def test_get_shop_with_street_not_in_city(self):
        """Проверка фильтрации по городу и улице, если улицы нет в данном
           городе"""
        params = '?street=West St&city=Los Santos'
        response: Response = self.client.get('/shop/'+params)
        self.assertEqual(response.status_code, 400)

    @patch('api.utils.now_time')
    def test_post_valid_shop(self, now_time_mock):
        """Проверка добавления валидного магазина"""
        now_time_mock.return_value = datetime.strptime('15:00', '%H:%M').time()
        data = self.valid_data()
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 200)
        data['is_open'] = True
        data['time_open'] = "10:00:00"
        data['time_close'] = "22:00:00"
        for field, value in data.items():
            self.assertEqual(response.data[field], value)

    def test_post_same_shop_name_dif_street(self):
        """Проверка добавления существующего названия магазина на другой
           улице"""
        data = self.valid_data()
        data['name'] = self.shop_on_main_st_in_los_santos.name
        data['city'] = self.shop_on_main_st_in_las_venturas.city
        data['street'] = self.shop_on_main_st_in_las_venturas.street
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_same_shop_name(self):
        """Проверка ошибки на добавление существующего назавния магазина
           на той же улице в том же городе"""
        data = self.valid_data()
        data['name'] = self.shop_on_main_st_in_los_santos
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_name(self):
        """Проверка ошибки при создании магазина с невалидным именем"""
        data = self.valid_data()
        data['name'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

        data['name'] = ''
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_city(self):
        """Проверка ошибки при создании магазина с несуществующим городом
           в базе"""
        data = self.valid_data()
        data['city'] = 'San Andreas'
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_street(self):
        """Проверка ошибки при создании магазина с несуществующей улицей
           в городе"""
        data = self.valid_data()
        data['street'] = 'Blabla St'
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

        data['city'] = self.shop_on_main_st_in_los_santos.city
        data['street'] = 'Blabla St'
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_house_number(self):
        """Проверка ошибки при создании магазина с невалидным номером дома"""
        data = self.valid_data()
        data['house_number'] = 666
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)
        data['house_number'] = 0
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)
        data['house_number'] = -11
        response: Response = self.client.post('/shop/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_time(self):
        """Проверка ошибки при создании магазина с невалидным временем"""
        data = self.valid_data()
        for period in ('time_open', 'time_close'):
            data[period] = '25:00'
            response: Response = self.client.post('/shop/', data=data)
            self.assertEqual(response.status_code, 400)
            data[period] = '-11:22'
            response: Response = self.client.post('/shop/', data=data)
            self.assertEqual(response.status_code, 400)
            data[period] = '11:666'
            response: Response = self.client.post('/shop/', data=data)
            self.assertEqual(response.status_code, 400)

    def test_post_missing_field(self):
        """Проверка ошибки при создании магазина с отсутвующим полем"""
        data = self.valid_data()
        for field in list(data):
            value = data.pop(field)
            response: Response = self.client.post('/shop/', data=data)
            self.assertEqual(response.status_code, 400)
            data[field] = value

    def valid_data(self) -> dict:
        """Возвращает валидные данные для Shop"""
        data = {
                "city": "Los Santos",
                "street": "Main St",
                "house_number": 1,
                "time_open": "10:00",
                "time_close": "22:00"
                }
        data['name'] = ''.join(random.choices(string.ascii_lowercase, k=8))
        return data
