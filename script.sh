#!/bin/bash
docker compose up --wait
docker exec prod-app /bin/bash -c "python manage.py makemigrations"
sleep 15
docker exec prod-app /bin/bash -c "python manage.py migrate"
docker exec -it prod-app /bin/bash -c "python manage.py collectstatic"
docker exec -it prod-app sh -c "python manage.py createsuperuser"
