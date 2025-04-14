# 📊 Attribution Modeling Project

Этот проект предназначен для анализа эффективности маркетинговых каналов с использованием различных моделей атрибуции.

## 📥 Входные данные

- `costs.csv` — расходы по каналам  
- `visits.csv` — визиты пользователей с указанием каналов и сессий  
- `orders.csv` — заказы пользователей с датами  

## Реализованные модели атрибуции

- **First Touch** — вся заслуга отнесена к первому каналу  
- **Last Touch** — заслуга отнесена к последнему каналу  
- **Linear Touch** — заслуга делится поровну между всеми каналами во воронке  
- **Марковская модель (Markov Model)** — модель на основе цепей Маркова, учитывающая вероятность переходов между каналами  

В результате обработки создаётся CSV-файл со следующей структурой:

```csv
channel_name,variable,value
AdNonSense,first_touch,2.0
LeapBob,first_touch,3.0
...
YRabbit,markov_model,11.07

```

## Требования

Перед запуском проекта убедитесь, что у вас установлены:

- **Docker** (с поддержкой Docker Compose)  
  [Скачать Docker](https://docs.docker.com/get-started/get-docker/)
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

### 2. Получение результата

#### Результат будет создан в директории output в формате csv

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



