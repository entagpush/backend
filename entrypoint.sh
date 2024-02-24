#!/bin/sh
# Exit if any command fails
set -e

# Use wait-for-it.sh to wait for the db service to be ready
./wait-for-it.sh db:5432 --timeout=120

# Then, proceed to apply database migrations
python manage.py migrate

# Start the application
exec "$@"
