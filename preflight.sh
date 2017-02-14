#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit
fi

cd sql
psql $1 -f creat_tables.sql
curl -0 https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xzf osnap_legacy.tar.gz
bash ./import_data.sh $1 5432
rm -rf osnap_legacy osnap_legacy.tar.gz
cd ..

cp -R src/* $HOME/wsgi
cp util/osnap_crypto.py $HOME/wsgi
