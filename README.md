# Финальный проект по API  
Проект api_yamdb - учебный проект курса "backend-python" Яндекс-Практикума


## Используемые технологии и библиотеки:
+ Python 3.7
+ Django 2.2
+ Django REST framework 3.12
+ Simple JWT 4.7
+ SQLite3


## Установка:
+ Клонировать репозиторий на локальную машину
+ Создать виртуальное окружение: $ python -m venv venv
+ Установить зависимости: $ pip install -r requirements.txt
+ Примененить миграций: $ python manage.py migrate
+ Запустить django сервер: $ python manage.py runserver


## Документация:
[ReDoc](http://127.0.0.1:8000/redoc/)


## Заполнение базы данных из CSV:
$ python manage.py loadtestdata


## Примеры запросов к API:
+ Получить список всех постов (GET): http://127.0.0.1:8000/api/v1/posts/
+ Получить определенный пост (GET): http://127.0.0.1:8000/api/v1/posts/1/
+ Получить коментарии определенного поста (GET): http://127.0.0.1:8000/api/v1/posts/1/comments/
+ Получить определенный коментарии к посту (GET): http://127.0.0.1:8000/api/v1/posts/1/comments/1/
+ Получить список всех групп (GET): http://127.0.0.1:8000/api/v1/groups/
+ Создать новый пост (требуется аутентификация) (POST): http://127.0.0.1:8000/api/v1/posts/


## Разработчики:
+ [Евгения Почуева](https://github.com/Eugen-bal)
+ [Сергей Елисеев](https://github.com/Serge170)
+ [Сергей Журавлев](https://github.com/geocrane)

