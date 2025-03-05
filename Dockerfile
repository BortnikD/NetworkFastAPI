# Используем официальный образ Python
FROM python:3.13.1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /src

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000 для работы FastAPI
EXPOSE 8000

# Запускаем сервер Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
