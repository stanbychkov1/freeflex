# Freeflex

![Freeflex]

Freeflex: API, позволяющий пользователям получить доступ к курсам и их материалам.

## Требования

1. Docker ([установка](https://docs.docker.com/engine/install/))
2. Docker-compose ([установка](https://docs.docker.com/compose/install/))

## Запуск приложения

Для запуска приложения склонируйте репозиторий с проектом:

```bash
git clone git@github.com:stanbychkov/freeflex.git
````
Затем создать .env файл с переменными и заполните все поля значениями, где есть <>:
````
DJANGO_SECRET_KEY='<secret_key>'
DJANGO_DEBUG=false
DOMAIN_NAME=localhost
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<postgres_username>
POSTGRES_PASSWORD=<postgres_password>
DB_HOST=db
DB_PORT=5432
````
После следует запустить приложение с помощью команды docker-compose, находясь в корневой папке проекта:
```bash
docker-compose up --build
````
Полсе запуска контейнера в командной строке в корневом каталоге приложения нужно выполнить следующие команды для создания администратора(superuser)
```bash
docker ps
````
Найти id контейнера freeflex_web и выполнить комманду:
```bash
docker exec -it <container_id> bash
````
Далле внутри контейнера выполните следующую комманду и действовать по указаниям системы:
```bash
python manage.py createsuper -u <username>
````
Воспользуетесь Swagger, чтоб увидеть полные возможности API.\
## Основные end-points:
[localhost/admin/](localhost/admin/) - административная часть\
[localhost/swagger/](localhost/swagger/) - документация Swagger\
[localhost/redoc/](localhost/redoc/) - документация Redoc\
[localhost/register/](localhost/register/) - регистрация пользователей\
[localhost/token/](localhost/token/) - получение токена\
[localhost/token/refresh/](localhost/token/refresh/) - замена токена\
[localhost/api/v1/courses/](localhost/api/v1/courses/) - доступ к списку курсов (без доступа к материалам)\
[localhost/api/v1/courses/id/](localhost/api/v1/courses/id/) - доступ к курсу (без доступа к материалам)\
[localhost/api/v1/courses/id/subscribe/](localhost/api/v1/courses/id/subscribe/) - подписка на курс\
[localhost/api/v1/courses/id/rating/](localhost/api/v1/courses/id/rating/) - поставить оценку курсу\
[localhost/api/v1/subscribed_courses/](localhost/api/v1/subscribed_courses/) - доступ к материалам и курсам, на которые подписан пользователь\
