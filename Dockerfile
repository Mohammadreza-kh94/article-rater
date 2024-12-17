FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ["python", "manage.py", "migrate"]

EXPOSE 8000

CMD ["gunicorn", "articlerater.wsgi:application", "--bind", "0.0.0.0:8000"]
