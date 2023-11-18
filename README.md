# django_shop_data_bank


##### Стек: Python, Django, Postgresql
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

* Cоздать виртуальное окружение:
```
python3 -m venv env
```
* Активировать виртуальное окружение
Для Windows
```
source venv/scripts/activate
```
Для MacOS/Linux
```
source venv/bin/activate
```
* Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
* Выполнить миграции:
```
python manage.py migrate
```
* Запустить проект на локальном сервере:
```
python manage.py runserver
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
POST http://localhost:8000/city/
```
```
curl -X POST "http://localhost:8000/city/"
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

##### Тесты
* Для запуска тестов используйте команду:
```
python manage.py test
```
Или
```pytest```


#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
