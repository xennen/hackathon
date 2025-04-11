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

#### 1. Если вы хотите получить результат в Telegram, то нужно заполнить файл config.json и указать нужный формат csv/xlsx

```json
{
    "service": "Telegram",
    "output_file_format": "xlsx"
}

```

1. Нужно зайти в телеграм и создать бота в этом боте: @BotFather и получить его токен
2. Токен нужно записать в файл .env в переменную BOT_TOKEN
3. Нужно получить свой ID в этом боте: @userinfobot
4. ID нужно записать в файл .env в переменную CHAT_ID
5. Активировать своего бота которого вы создали в пункте 1 (найти его в поиске и нажать Start)

Пример .env файла:

```bash
BOT_TOKEN=1234467657:DRaRb4346n6725nb5232b634
CHAT_ID=123545678
```

#### 2. Если вы хотите получить результат в S3, то нужно заполнить файл config.json и указать нужный формат csv/xlsx

```json
{
    "service": "S3",
    "output_file_format": "xlsx"
}

```

1. Нужно получить из S3: ACCESS_KEY, SECRET_KEY, BUCKET_NAME
2. Добавить их в .env файл

Пример .env файла:

```bash
ACCESS_KEY=YIyRfgfZ1Febreb4n75m7wcer
SECRET_KEY=rerbeDSb3555nwgbrsTRTNRETVEREVSRE345
BUCKET_NAME=s3-model
```

### 3. Запуск через Docker Compose

Соберите и запустите контейнеры в фоновом режиме:

```bash
docker-compose up -d --build
```



