#Финальный проект по API

##Описание:

####Проект api_yatube - это API социальной сети yatube.

Yatube - это учебный проект курса "backend-python" от Яндекс-Практикума.

#####Реализован функционал дающий возможность: -Подписываться на пользователя. -Просматривать, создавать новые, удалять и изменять посты. -Просматривать и создавать группы. -Комментировать, смотреть, удалять и обновлять комментарии. -Фильтровать по полям. К API есть документация по адресу http://localhost:8000/redoc/

##Установка:

Клонируем репозиторий на локальную машину:

$ git clone https://github.com/Serge170/api_final_yatube Создаем виртуальное окружение:

$ python -m venv venv Устанавливаем зависимости:

$ pip install -r requirements.txt Создание и применение миграций:

$ python manage.py makemigrations и $ python manage.py migrate Запускаем django сервер:

$ python manage.py runserver #####Все готово к использованию API!

% ##Примеры запросов к API: Получить список всех постов (GET): http://127.0.0.1:8000/api/v1/posts/

% Получить определенный пост (GET): % http://127.0.0.1:8000/api/v1/posts/1/

% Получить коментарии определенного поста (GET): % http://127.0.0.1:8000/api/v1/posts/1/comments/

% Получить определенный коментарии к посту (GET): % http://127.0.0.1:8000/api/v1/posts/1/comments/1/

% Получить список всех групп (GET): % http://127.0.0.1:8000/api/v1/groups/

% Создать новый пост (POST): % (Требуется аутентификация) http://127.0.0.1:8000/api/v1/posts/
