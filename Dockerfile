FROM python:alpine

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

# Установим директорию для работы
WORKDIR /birthdays_lazarevskoe_bot_2

COPY ./requirements.txt ./

# Устанавливаем зависимости и gunicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Копируем файлы и билд
COPY ./ ./

RUN chmod -R 777 ./