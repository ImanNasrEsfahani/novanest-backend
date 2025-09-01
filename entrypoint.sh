#!/bin/bash

# Wait for DB to be ready
echo "Database Host: $DB_HOST"
echo "Database Port: $DB_PORT"
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Database is up - running migrations..."
python manage.py makemigrations
python manage.py makemigrations forms
python manage.py migrate

echo "Starting server..."
exec "$@"
