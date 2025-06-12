#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate

echo "Loading initial data from fixture..."
python manage.py loaddata initial_data.json || echo "Aucune donnée chargée ou erreur lors du loaddata."

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
