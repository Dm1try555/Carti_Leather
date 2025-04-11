FROM python:3.10-slim

WORKDIR /app

# Устанавливаем необходимые пакеты для работы с PostgreSQL и другими зависимостями
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    gettext \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы в контейнер
COPY . .

# Выполняем миграции и запускаем gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn OnlineStore.wsgi:application --bind 0.0.0.0:8000"]
