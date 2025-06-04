FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN sed -i '/^mkl_fft==/d' requirements.txt \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput \
 && python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "lava_api.wsgi:application", "--bind", "0.0.0.0:8000"]
