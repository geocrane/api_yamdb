#Финальный проект по API
Проект api_yamdb - учебный проект курса "backend-python" от Яндекс-Практикума.


#Используемые пакеты:
requests==2.26.0
django==2.2.16
djangorestframework==3.12.4
django-filter==21.1
djangorestframework-simplejwt==4.7.2
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3


##Установка:
Клонируем репозиторий на локальную машину:
$ git clone https://github.com/Serge170/api_final_yatube Создаем виртуальное окружение:
$ python -m venv venv Устанавливаем зависимости:
$ pip install -r requirements.txt Создание и применение миграций:
$ python manage.py makemigrations и $ python manage.py migrate Запускаем django сервер:
$ python manage.py runserver #####Все готово к использованию API!


##Документация ReDoc:
http://127.0.0.1:8000/redoc/


##Примеры запросов к API:
Получить список всех постов (GET): http://127.0.0.1:8000/api/v1/posts/
Получить определенный пост (GET): % http://127.0.0.1:8000/api/v1/posts/1/
Получить коментарии определенного поста (GET): % http://127.0.0.1:8000/api/v1/posts/1/comments/
Получить определенный коментарии к посту (GET): % http://127.0.0.1:8000/api/v1/posts/1/comments/1/
Получить список всех групп (GET): % http://127.0.0.1:8000/api/v1/groups/
Создать новый пост (POST): % (Требуется аутентификация) http://127.0.0.1:8000/api/v1/posts/


##Разработчики:
Евгения Почуева - git: https://github.com/Eugen-bal
Сергей Елисеев - git: https://github.com/Serge170
Сергей Журавлев - git: https://github.com/geocrane

