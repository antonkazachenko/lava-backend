FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static for DRF’s browsable API
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Note the “:application” so Gunicorn knows what callable to run
CMD ["gunicorn", "lava_api.wsgi:application", "--bind", "0.0.0.0:8000"]
