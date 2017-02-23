#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit
fi

apachectl stop
#pg_ctl -D $HOME/cis322/sql/data stop

cd sql
pg_ctl -D $HOME/cis322/sql/data/ -l logfile start
dropdb $1
createdb $1
psql $1 -f create_tables.sql
cd ..

cp -R src/* $HOME/wsgi/

apachectl start
apachectl restart
