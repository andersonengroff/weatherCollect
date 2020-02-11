#!/bin/sh
docker-compose down -v
docker-compose up -d --build
echo "creating data base"
docker-compose exec app python manage.py create_db
echo "seeding data base"
docker-compose exec app python manage.py seed_db
docker-compose exec app pytest