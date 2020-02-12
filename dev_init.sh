#!/bin/sh
docker-compose down -v
docker-compose up -d --build
echo "creating data base"
docker-compose exec app python manage.py create_db
echo "seeding data base"
docker-compose exec app python manage.py seed_db
docker-compose exec app pytest
echo "starting cron jobs"
crontab <<'EOF'
SHELL=/bin/bash
#min hr md mo wkday command
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/7284876
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/weather/collect/7284876
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/2640729
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/weather/collect/2640729
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/2653822
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/weather/collect/2653822
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/2638111
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/weather/collect/2638111
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/forecast/collect/2644581
*/1 *  *  *  *     curl -H "Content-Type: application/json" -X POST http://localhost:5000/weather/collect/2644581
*/10 *  *  *  *    curl -H "Content-Type: application/json" -X POST http://localhost:5000/transformation/fact
EOF