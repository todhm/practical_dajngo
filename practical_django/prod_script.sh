#!/bin/bash 
export PATH=/app/.heroku/node/bin:$PATH 
npm run build-prod 
./manage.py collectstatic --noinput 
./manage.py migrate --noinput 
./manage.py test --exclude-tag=e2e
