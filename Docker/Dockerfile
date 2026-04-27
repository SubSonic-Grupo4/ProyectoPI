FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY pages ./pages
COPY js ./js
COPY css ./css
COPY smoke_test.py .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.controller.controller:app", "--host", "0.0.0.0", "--port", "8000"]
