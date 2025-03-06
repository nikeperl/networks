# Базовый образ
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запуск сервера
CMD ["python3", "main.py"]
