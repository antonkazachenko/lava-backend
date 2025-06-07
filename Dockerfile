# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install the simplified Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# This is the most important step:
# It copies ALL your files (your Python code AND predicted_topics.csv)
# into the container.
COPY . .

# Collect static files for Django REST Framework's browsable API
RUN python manage.py collectstatic --noinput

# Tell Docker that the container listens on port 8000
EXPOSE 8000

# Start the Gunicorn web server when the container launches
CMD ["gunicorn", "lava_api.wsgi", "--bind", "0.0.0.0:8000"]