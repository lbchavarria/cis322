#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <output dir>"
	exit
fi

if [ -d $2 ]; then
	rm -r $2/*
	echo "Directory emptied"
else
	mkdir $2
fi

cd ../sql
pg_ctl -D $HOME/cis322/sql/data -l logfile start
psql -v dir=$2
psql $1 -f ../sql/export_data.sql

cd ..
