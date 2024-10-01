#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
echo "Running migrations..."
python manage.py migrate

# Start the Django server
echo "Generating statics..."
python manage.py collectstatic --no-input --clear

echo "Starting server..."
if [ "$DEBUG" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  gunicorn app.wsgi:application --bind 0.0.0.0:8000
fi