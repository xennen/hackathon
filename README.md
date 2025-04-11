# Атрибутивная модель в Docker

Этот проект представляет собой модель атрибуции, которая работает внутри Docker контейнера с использованием **Docker Compose**.

## Требования

Перед запуском проекта убедитесь, что у вас установлены:

- **Docker** (с поддержкой Docker Compose)  
  [Скачать Docker](https://www.docker.com/products/docker-desktop)
- **Docker Compose** (если не встроен в вашу версию Docker)  
  [Инструкция по установке](https://docs.docker.com/compose/install/)

---

## Шаги для запуска проекта

### 1. Клонируйте репозиторий

Выполните в терминале:

```bash
git clone https://github.com/xennen/hackathon.git
cd hackathon
```

### 2. Настройка получения результата

Если вы хотите получить результат в Telegram, то нужно заполнить файл config.json и указать нужный формат csv/xlsx

```json
{
    "service": "Telegram",
    "output_file_format": "xlsx"
}

```

1. Нужно зайти в телеграм и создать бота в этом боте: @BotFather и получить его токен
2. Нужно получить свой id в этом боте: @userinfobot
3. Активировать своего бота которого вы создали в пункте 1 (найти его в поиске и нажать Start)

### 3. Запуск через Docker Compose

Соберите и запустите контейнеры в фоновом режиме:

```bash
docker-compose up -d --build
```



