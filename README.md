# vending-machine
# Название проекта

## Описание
Краткое описание вашего проекта, его назначение и основные возможности.

## Содержание
- [Требования](#требования)
- [Установка](#установка)
  - [Стандартная установка](#стандартная-установка)
  - [Установка с Docker](#установка-с-docker)
- [Запуск](#запуск)
  - [Стандартный запуск](#стандартный-запуск)
  - [Запуск с Docker](#запуск-с-docker-compose)
- [Конфигурация](#конфигурация)
- [API Документация](#api-документация)

## Требования

### Для стандартной установки
- Python 3.8+
- pip

### Для установки с Docker
- Docker 
- Docker Compose 

## Установка

### Стандартная установка

1. Клонируйте репозиторий:
```bash
  git clone https://github.com/AnvarS21/vending-machine.git
  cd vending-machine
```

2. Установите зависимости:
```bash
  pip install -r requirements.txt
```

3. Настройте окружение:
```bash
  cp .env_example .env
# Отредактируйте .env файл с вашими настройками
```

### Установка с Docker

1. Клонируйте репозиторий:
```bash
  git clone https://github.com/AnvarS21/vending-machine.git
  cd vending-machine
```

2. Настройте окружение:
```bash
  cp .env_example .env
# Отредактируйте .env файл с вашими настройками
```

## Запуск

### Стандартный запуск

```bash
  python manage.py runserver
```

### Запуск с Docker-compose

```bash
  docker-compose up --build
```

## Конфигурация

Описание основных настроек в файле .env:

| Переменная | Описание                  | Пример значения |
|------------|---------------------------|-----------------|
| ALLOWED_HOSTS | Хост базы данных          | localhost или * |
| SECRET_KEY | Секретный ключ приложения | your-secret-key |
| DEBUG | Режим отладки             | True/False      |
| DJANGO_SUPERUSER_USERNAME | Имя суперпользователя     | admin           |
| DJANGO_SUPERUSER_EMAIL | Почта суперпользоваля     | admin@gmail.com |
| DJANGO_SUPERUSER_PASSWORD | Пароль суперпользователя  | admin           |

## API Документация
http://{host}/swagger/

host - (обычно) 127.0.0.1:8000
