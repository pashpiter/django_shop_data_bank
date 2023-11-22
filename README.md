# django_shop_data_bank


##### Стек: Python, Django, sqlite3
***

### Что умеет django_shop_data_bank
* Просмотр доступных городов
* Просмотр доступных улиц города
* Просмотр всех доступных в базе магазинов, с возможностью фильтрации по городу, улице или параметру "открыт в данный момент или закрыт"

### Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/django_shop_data_bank.git
```
* Перейти в папку django_shop_data_bank

* Запустить проект используя docker-compose
```
sudo docker-compose up -d
```

### Примеры команд API
* Проверка работы приложения
```
GET http://localhost:8000/
```
```
curl "http://localhost:8000/"
```
* Получение списка городов
```
GET http://localhost:8000/city/
```
```
curl -X GET "http://localhost:8000/city/"
```
* Получение списка улиц города
```
GET http://localhost:8000/city/{city_id}/street/
```
```
curl "http://localhost:8000/city/{city_id}/street/"
```
* Получение списка магазинов
```
GET http://localhost:8000/shop/
```
```
curl "http://localhost:8000/shop/"
```
* Получение списка магазинов с доп параметрами (параметры могут отсутствовать или быть не все)
```
GET http://localhost:8000/shop/?street={str}&city={str}&open={int(0/1)}
```
```
curl "http://localhost:8000/shop/?street={str}&city={str}&open={int(0/1)}"
```
* Добавление магазина
```
POST http://localhost:8000/shop/
{
    "name": "str", (Shop)
    "city": "str", (Los Santos)
    "street": "str", (Main St)
    "house_number": int, (11)
    "time_open": "str", (9:00)
    "time_close": "str" (21:00)
}
```
```
curl -X POST \
--location 'http://localhost:8000/shop/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Pole",
    "city": "Los Santos",
    "street": "Main St",
    "house_number": 1,
    "time_open": "21:00",
    "time_close": "9:00"
}'
```

##### Тесты
* Для запуска тестов используйте команду:
```
python manage.py test
```
Или
```pytest```


#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
