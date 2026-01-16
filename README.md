# w1tish

**Prerequisites**:
- **macOS / Linux**: `git`, `docker` (или `docker-engine`) и `docker-compose` (или Docker Desktop).
- **Windows**: Docker Desktop (рекомендуется) или Docker Engine + Docker Compose, и `git`.
- **Python** (для локальной разработки бекенда): Python 3.10+ (проверяйте `python --version`).

**Quick start (Docker, кросс-платформенно)**

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/KIriLOsck/w1tish.git
cd w1tish
```

2. Убедитесь, что Docker (или Docker Desktop) запущен.

3. Поднять сервисы:

```bash
docker-compose up --build
```

4. После старта сервисов:
- Фронтенд будет доступен по http://localhost/
- Бекенд (FastAPI) на http://localhost:8000
- Postgres на порту 5432 (если нужен внешний доступ)

5. Остановка и удаление контейнеров:

```bash
docker-compose down
```

Полезные команды Docker:

```bash
docker-compose logs -f        # прослушать логи
docker-compose up -d         # запустить в фоне
docker-compose down --volumes # удалить и тома
```

**Локальная разработка — Backend (без Docker)**

1. Перейдите в папку `backend`:

```bash
cd backend
```

2. macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# Запуск сервера
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

3. Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
# Запуск сервера
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Windows (cmd.exe):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Примечание: в `backend/requirements.txt` перечислены зависимости (FastAPI, Uvicorn, SQLAlchemy и т.д.).

**Локальная разработка — Frontend**

Файлы фронтенда находятся в папке `frontend`. Для разработки можно просто открыть `frontend/index.html` в браузере или поднять простой HTTP-сервер:

macOS / Linux / Windows (через Python):

```bash
cd frontend
python3 -m http.server 8080
# затем открыть http://localhost:8080
```

Или использовать любой статический сервер / live-reload плагин в редакторе.

**Настройка базы данных**

Docker Compose автоматически использует файл `init.sql` (см. `docker-compose.yml`) при первом старте контейнера Postgres. При локальном использовании Postgres вы можете применить `init.sql` вручную.

**Переменные окружения**

Настройки для контейнеров задаются через переменные окружения (см. `docker-compose.yml`): `DB_USER`, `DB_PASS`, `JWT_SECRET` и т.д. Можно создать файл `.env` в корне репозитория с нужными значениями, например:

```env
DB_USER=admin
DB_PASS=admin
JWT_SECRET=supersecretkey
```

Docker Compose автоматически подхватит `.env` при запуске.

**Частые проблемы и их решения**

- Порт 8000 или 80 уже занят: остановите процесс, который их использует, или измените проброс портов в `docker-compose.yml`.
- Docker Desktop не запускается на Windows/macOS: убедитесь, что ваша система поддерживает виртуализацию и запущены необходимые службы.
- При ошибках зависимостей в локальном venv: обновите `pip`, удалите и пересоздайте виртуальное окружение.

**Полезные команды для отладки**

```bash
# Просмотр запущенных контейнеров
docker ps

# Просмотр логов конкретного сервиса
docker-compose logs backend

# Подключиться к запущенному контейнеру
docker exec -it <container_id_or_name> /bin/sh
```

