FROM python:3.12-slim

# Отключаем буферизацию вывода
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libc6 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements
COPY requirements.txt .

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Запуск бота
CMD ["python", "whatsapp_bot.py"]
