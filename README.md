# Сервис планирования домашнего меню

Полное описание в процесе разработки

## Запуск проекта

### Установка Django
Скачайте код в нужную директорию:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```

Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Создать файл `.env` и положите туда код вида:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

### MEDIA-файлы

Загрузите файлы в папку ``/media``:

https://drive.google.com/drive/folders/1XbMnu-7VB3wPndqQfEC1rcPIGxirpC2f?usp=sharing

### Запуск

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран.
