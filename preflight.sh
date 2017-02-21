#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit
fi

cd sql
psql $1 -f create_tables.sql
cd ..

cp -R src/* $HOME/wsgi

apachectl start
apachectl restart
