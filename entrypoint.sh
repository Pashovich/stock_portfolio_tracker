#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for the PostgreSQL database to be available
echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Run database migrations
echo "Running migrations..."
python manage.py migrate

# Start the Django server
echo "Generating statics..."
python manage.py collectstatic --no-input --clear

echo "Starting server..."
gunicorn app.wsgi:application --bind 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000