# profile_project
## Task-Backend-1
### Описание:
Profile API - проект личного кабинета пользователя

### Технологии:

[![name badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![name badge](https://img.shields.io/badge/Django-3776AB?logo=django&logoColor=white)](https://docs.djangoproject.com/en/4.2/releases/3.2/)
[![name badge](https://img.shields.io/badge/Django_REST_framework-3776AB?logo=djangorestramework&logoColor=white)](https://www.django-rest-framework.org/)

### Как запустить проект:

Установить Docker Compose:

```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
```
Cоздать папку проекта и перейти в нее:
```
mkdir profile
cd profile
```
Создать файл .env и заполните его своими данными, пример:

```
POSTGRES_DB=profile # Имя_БД
POSTGRES_USER=profile_user # Имя пользователя БД
POSTGRES_PASSWORD=profile_password # Пароль к БД
DB_NAME=profile
DB_HOST=db # Адрес, по которому Django будет соединяться с БД
DB_PORT=5432 # Порт соединения к БД
SECRET_KEY=*** # Секретный ключ Django (без кавычек).
ALLOWED_HOSTS=*** # Список разрешённых хостов (через запятую и без пробелов)
DEBUG=False # Выбрать режим отладки
EMAIL_HOST_USER=Admin@mail.com # Emeil для отправки OTP кодов
BROKER_URL=redis://redis:6379/0
RESULT_BACKEND=redis://redis:6379/0
```

Скачать файл docker-compose.yml и запустить его:

```
sudo docker compose -f docker-compose.yml up
```

Создать и выполнить миграции, создать суперпользователя, собрать статические файлы бэкенда и скопировать их:

```
sudo docker compose -f docker-compose.yml exec backend python manage.py makemigrations
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/static/. /static/static/ 
```
