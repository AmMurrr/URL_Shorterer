

# URL SHORTERER


## Что это?
Небольшой проект практической направленности по созданию своего сокращателя ссылок, аналога Tiny URL и подобных сервисов.

Проект состоит из API и БД.

## Основной Стек

- Python
- FastAPI
- MongoDB
- Docker

## Настройка MongoDB

По умолчанию приложение ожидает MongoDB на `mongodb://localhost:27017`.

Поддерживаются переменные окружения:

- `MONGO_URI` 
- `MONGO_DB_NAME` (по умолчанию `mytinyurl`)
- `MONGO_URL_COLLECTION` (по умолчанию `urls`)
- `MONGO_COUNTER_COLLECTION` (по умолчанию `counters`)

Запуск:

```bash
uvicorn app.main:app --reload
```


