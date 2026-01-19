FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /frontend ./frontend
COPY /backend ./backend
COPY /tests /tests
COPY main.py .
COPY pytest.ini .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]