### Описание проекта:

Проект представляет собой API для работы с постами, комментариями, группами и подписками пользователей. Он разработан на основе фреймворка Django и библиотеки Django REST Framework. Проект позволяет пользователям создавать, редактировать и удалять посты, оставлять комментарии к постам, подписываться на других пользователей и просматривать группы.

### Проект использует следующий стек технологий:

* Python
* Django
* Django REST Framework

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Aleskerovz/api_final_yatube.git
```

```
cd api_final_yatube
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python3 manage.py migrate
```

5. Запустить проект:

```
python3 manage.py runserver
```

### Где искать документацию к API:

Когда вы запустите проект, по адресу  http://127.0.0.1:8000/redoc/ будет доступна документация для API Yatube. В документации описано, как должен работать API. Документация представлена в формате Redoc.

### Создание пользователя для админки:
Для создания пользователя с правами администратора в Django, выполните следующую команду:
```
python manage.py createsuperuser
```

Затем следуйте инструкциям в терминале, чтобы указать имя пользователя, адрес электронной почты и пароль для администраторского аккаунта.

После успешного создания аккаунта вы сможете войти в административную панель Django, используя учетные данные администратора.
Административная панель будет доступна по адресу http://127.0.0.1:8000/admin/.

### Примеры запросов:

1. Получение списка групп (метод GET):
* URL: ```/api/v1/groups/```
* Результат:
```
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]
```
2. Получение списка постов (метод GET):
* URL: ```/api/v1/posts/```
* Результат:
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
3. Создание нового поста (метод POST):
* URL: ```/api/v1/posts/```
* Тело запроса (JSON):
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
* Результат:
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
4. Получение списка комментариев к посту (метод GET):
* URL: ```/api/v1/posts/{post_id}/comments/```
* Результат:
```
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```
5. Создание новой подписки на пользователя (метод POST):
* URL: ```/api/v1/follow/```
* Тело запроса (JSON):
```
{
  "following": "string"
}
```
* Результат:
```
{
  "user": "string",
  "following": "string"
}
```

### Информация об авторе:

Проект разработан и поддерживается Алескеровым Зауром. Вы можете связаться со мной по электронной почте: aleskerovz@ya.ru
