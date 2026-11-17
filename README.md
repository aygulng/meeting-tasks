# Задачи из встречи — локальная LLM

Учебный проект: запуск модели через Ollama и извлечение задач из русскоязычных заметок встречи. FastAPI + Pydantic + простой веб-интерфейс.

Meeting Tasks — учебный проект для автоматического извлечения задач, ответственных и сроков из заметок встречи. Обработка выполняется локальной LLM через Ollama, без передачи данных в облачные сервисы.

Технологии: Python, FastAPI, Ollama, Qwen3/Llama3, Pydantic, HTTPX, HTML, CSS, JavaScript и unittest.

## Запуск на Windows (PowerShell, Python 3.11+)

Откройте терминал в этой папке:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Установите [Ollama](https://ollama.com/download/windows), запустите приложение и скачайте модель:

```powershell
ollama pull qwen3:4b
ollama list
```

Если сервис не запущен, выполните `ollama serve` в отдельном терминале. Затем:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Откройте http://127.0.0.1:8001. Выберите модель, вставьте пример и извлеките задачи. Первичная загрузка модели может занять несколько минут. Модели приложение автоматически не скачивает.

## Запуск в Docker

В Docker Compose запускаются два контейнера: приложение и отдельная Ollama.
Порт Ollama не публикуется на компьютере и доступен только приложению внутри
Docker-сети. Из корня проекта выполните:

```powershell
docker compose up --build -d
docker compose exec ollama ollama pull qwen3:4b
```

Модель загружается один раз и сохраняется в Docker volume `ollama-data`.
После загрузки откройте http://127.0.0.1:8001. Посмотреть состояние, журнал и
остановить контейнеры можно командами:

```powershell
docker compose ps
docker compose logs -f
docker compose down
```

В `compose.yaml` приложение обращается к Ollama по внутреннему адресу
`http://ollama:11434`. Для обычного запуска без Docker адресом по умолчанию
остаётся `http://127.0.0.1:11434`; его можно переопределить переменной
окружения `OLLAMA_URL`.

## Проверка для демонстрации

1. Явная задача: «Анна подготовит отчёт к пятнице» — задача, Анна, «к пятнице» и дословная цитата.
2. Нет ответственного: «Нужно обновить инструкцию» — owner и deadline равны null.
3. Нет задач: «Обсудили погоду» — пустой список.
4. После загрузки модели отключите интернет и повторите запрос. Приложение обращается только к loopback; используйте локальную модель, не cloud.
5. Выполните `ollama ps` во время обработки: посмотрите загруженную модель и распределение CPU/GPU. Повторите один текст на другой установленной модели и сравните качество и скорость.

API: `GET /api/models`, `POST /api/extract` с полями text и model. Документация приложения: `/docs`.

Источники: https://docs.ollama.com/api/generate и https://docs.ollama.com/api/tags.

