#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit
fi

cd sql
pg_ctl -D data/ start
createdb $1
psql $1 -f create_tables.sql
cd ..

cp -R src/* wsgi/

apachectl start
apachectl restart
