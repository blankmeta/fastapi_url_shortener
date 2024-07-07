# Базовый сокращатель ссылок

Cервис для создания сокращённой формы передаваемых URL и анализа активности их использования.

## Тестирование

Запустите базу на порту 6000
```
docker run \
  --rm \
  --name postgres-fastapi-test \
  -p 6000:6000 \
  -e POSTGRES_USER=postgres \
  -e PGPORT=6000 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=collection \
  -d postgres:14.5
```

В корневой директории запустите тесты ```pytest -v```


## Переменные окружения

Шаблон наполнения файла .env в директории /src/

```
APP_TITLE="UrlShortener"
DATABASE_DSN=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
```
Или в файле ```/src/.env.example```
