#!/bin/bash

docker-compose exec app alembic -c /alembic/alembic.ini upgrade head
