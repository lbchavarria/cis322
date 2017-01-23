#!/bin/bash

read dbname
read port_num

create $dbname
psql $dbname -f create_tables.sql
curl https://classes.cs.uoregon.edu/17W/cis322/files/osnap_legacy.tar.gz > $HOME/sql/osnap_legacy.tar.gz
gunzip $HOME/sql/osnap_legacy.tar.gz
tar -xvf $HOME/sql/osnap_legacy.tar
psql $dbname -f load_data_tables.sql
