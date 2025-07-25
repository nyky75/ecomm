# Ecommpay QA Project

Проект с автотестами для API (FastAPI + SQLAlchemy), оформленными в стиле BDD с интеграцией Allure-отчётов.

---

## Установка и запуск

### 1. Подготовить окружение
Установи Docker и Docker Compose (Docker Desktop на macOS/Windows):
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Проверь, что всё работает:
```bash
docker --version
docker-compose --version
```

### 2. Сборка проекта 
```bash
make build
```

### 3. Запуск тестов
```bash
make test
```

### 4. Генерация allure репорта
```bash
make report
```
Allure репорт будет доступен по адресу - http://localhost:5050/allure-docker-service/latest-report

### 5. Остановка контейнеров
```bash
make down
```

