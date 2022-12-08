# Выгрузка каталога товаров из csv-файла с сохранением всех позиций в базе данных

## Задание

Есть некоторый [csv-файл](./phones.csv), который выгружается с сайта-партнера. Этот сайт занимается продажей телефонов.

Мы же являемся их региональными представителями, поэтому нам необходимо взять данные из этого файла и отобразить их на нашем сайте на странице каталога, с их предварительным сохранением в базу данных.


## Решение  

Создаю базу данных в СУБД PostgreSQL:  
```
$ psql
psql (13.8 (Debian 13.8-0+deb11u1))
Введите "help", чтобы получить справку.

postgres=# ALTER USER postgres with PASSWORD 'postgres';
ALTER ROLE
postgres=# CREATE DATABASE netology_import_phones;
CREATE DATABASE
```

Корректирую секцию DATABASES в файле settings.py для подключения к PostgreSQL.


Создаю в приложении модель Phone:  
```
from django.db import models

class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    image = models.ImageField()
    relese_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField()
```

Создаю файл миграции ( первый шаг миграции ):  
```
$ python3 manage.py makemigrations
Migrations for 'phones':
  phones/migrations/0001_initial.py
    - Create model Phone

```

Создаю таблицу в БД ( второй шаг миграции ):  
```
$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, phones, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying phones.0001_initial... OK
  Applying sessions.0001_initial... OK
```

В результате получаю следующую структуру в БД:  
```
netology_import_phones=# \dt
                     Список отношений
 Схема  |            Имя             |   Тип   | Владелец 
--------+----------------------------+---------+----------
 public | auth_group                 | таблица | postgres
 public | auth_group_permissions     | таблица | postgres
 public | auth_permission            | таблица | postgres
 public | auth_user                  | таблица | postgres
 public | auth_user_groups           | таблица | postgres
 public | auth_user_user_permissions | таблица | postgres
 public | django_admin_log           | таблица | postgres
 public | django_content_type        | таблица | postgres
 public | django_migrations          | таблица | postgres
 public | django_session             | таблица | postgres
 public | phones_phone               | таблица | postgres
(11 строк)

```

В файл [import_phones.py](phones/management/commands/import_phones.py) в метод добавляю следующий код:  
```
for phone in phones:
    new_phone = Phone.objects.create(
        id=int(phone['id']),
        name=phone['name'],
        price=int(phone['price']),
        image=phone['image'],
        release_date=phone['release_date'],
        lte_exists=phone['lte_exists'],
        slug=slugify(phone['name'])
    )
```

Загружаю данные в БД:  
```
$ python manage.py import_phones
```

Содержимое таблицы после загрузки данных:  
```
netology_import_phones=# select * from phones_phone;
 id |         name          |  price   |                                       image                                        | release_date | lte_exists |         slug          
----+-----------------------+----------+------------------------------------------------------------------------------------+--------------+------------+-----------------------
  1 | Samsung Galaxy Edge 2 | 73000.00 | https://avatars.mds.yandex.net/get-mpic/364668/img_id5636027222104023144.jpeg/orig | 2016-12-12   | t          | samsung-galaxy-edge-2
  2 | Iphone X              | 80000.00 | https://avatars.mds.yandex.net/get-mpic/200316/img_id270362589725797013.png/orig   | 2017-06-01   | t          | iphone-x
  3 | Nokia 8               | 20000.00 | https://avatars.mds.yandex.net/get-mpic/397397/img_id6752445806321208103.jpeg/orig | 2013-01-20   | f          | nokia-8
(3 строки)

```

В [views.py](phones/views.py) помешаю код, отвечающий за вывод списка товаров, сортировку и вывод конкретного товара.  
  
  
Список товаров:  

![Список телефонов](images/list_phones.png)


Товар:  

![Телефон](images/item_phone.png)


## Реализация

Что необходимо сделать:

- В файле `models.py` нашего приложения создаем модель Phone с полями `id`, `name`, `price`, `image`, `release_date`, `lte_exists` и `slug`. Поле `id` - должно быть основным ключом модели.
- Значение поля `slug` должно устанавливаться слагифицированным значением поля `name`.
- Написать скрипт для переноса данных из csv-файла в модель `Phone`.
  Скрипт необходимо разместить в файле `import_phones.py` в методе `handle(self, *args, **options)`.
  Подробнее про подобные скрипты (django command) можно почитать [здесь](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/) и [здесь](https://habr.com/ru/post/415049/).
- При запросе `<имя_сайта>/catalog` - должна открываться страница с отображением всех телефонов.
- При запросе `<имя_сайта>/catalog/iphone-x` - должна открываться страница с отображением информации по телефону. `iphone-x` - это для примера, данное значние берется из `slug`.
- В каталоге необходимо добавить возможность менять порядок отображения товаров: по названию (в алфавитном порядке) и по цене (по-убыванию и по-возрастанию).

Шаблоны подготовлены, ваша задача ознакомиться с ними и корректно написать логику.

## Ожидаемый результат

![Каталог с телефонами](res/catalog.png)

## Подсказка

Для переноса данных из файла в модель можно выбрать один из способов:

- воспользоваться стандартной библиотекой языка python : `csv` (рекомендуется).
- построчно пройтись по файлу и для каждой строки сделать соответствующую запись в БД.

Для реализации сортировки можно - брать параметр `sort` из `request.GET`.

Пример запросов:

- `<имя_сайта>/catalog?sort=name` - сортировка по названию.
- `<имя_сайта>/catalog?sort=min_price` - сначала отображать дешевые.

## Документация по проекту

Для запуска проекта необходимо:

Установить зависимости:

```bash
pip install -r requirements.txt
```

Выполнить следующие команды:

- Команда для создания миграций приложения для базы данных

```bash
python manage.py migrate
```

- Команда для загрузки данных из csv в БД

```bash
python manage.py import_phones
```

- Команда для запуска приложения

```bash
python manage.py runserver
```

- При создании моделей или их изменении необходимо выполнить следующие команды:

```bash
python manage.py makemigrations
python manage.py migrate
```
