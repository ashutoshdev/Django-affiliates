#!/usr/bin/env bash

if [ -z $1 ]; then
    BRANCH=release
else
    BRANCH=$1
fi;

python manage.py migrate <appname>
git fetch
git reset --hard origin/$BRANCH
python3 manage.py collectstatic --noinput
supervisorctl restart live_affiliates
#before start activate the bin/activate

