#!/bin/bash

read dbname
echo $dbname
read port_num
echo $port_num

initdb -D $HOME/sql/home
echo "init"
pg_ctl -D $HOME/sql/home -o "-p $port_num" -l $HOME/sql/logfile start
echo "start"

create $dbname
echo "create"
psql $dbname -f create_tables.sql
echo "psql"
curl https://classes.cs.uoregon.edu/17W/cis322/files/osnap_legacy.tar.gz > $HOME/sql/osnap_legacy.tar.gz
echo "curl"
gunzip $HOME/sql/osnap_legacy.tar.gz
echo "gunzip"
tar -xvf $HOME/sql/osnap_legacy.tar
echo "untar"
psql $dbname -f load_data_tables.sql
echo "finish"
