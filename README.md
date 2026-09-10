# Test FastAPI Service

Небольшой FastAPI-сервис для тестов и дальнейших модификаций. Данные хранятся
в памяти и сбрасываются при перезапуске приложения.

## Запуск

Требуется Python 3.11 или новее.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

После запуска доступны:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Эндпоинты

- `GET /` — приветствие
- `GET /health` — проверка состояния
- `GET /items` — список объектов
- `GET /items/{item_id}` — получение объекта
- `POST /items` — создание объекта
- `DELETE /items/{item_id}` — удаление объекта

Пример создания объекта:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/items `
  -ContentType application/json `
  -Body '{"name":"Demo","description":"Test item"}'
```

## Тесты

```powershell
pytest
```
