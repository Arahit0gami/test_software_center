# Используйте официальный образ Python с вашей предпочитаемой версией Python
FROM python:3.11.0

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Установите переменные окружения, необходимые для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

# Установите зависимости
RUN apt-get update
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте проект
COPY ./events_website .

# Запустите сервер приложений
CMD ["gunicorn", "-b", ":8000", "events_website.wsgi:application"]
