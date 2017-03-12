#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./import_data.sh <dbname> <imput dir>"
	exit
fi

cd ../sql
pg_ctl -D $HOME/cis322/sql/data -l logfile start
cd ../export/$2
VAR=$(pwd)
psql -d $1 -c "DROP TABLE IF EXISTS temp"
psql -d $1 -c "CREATE TABLE temp (username varchar(16) DEFAULT NULL, password varchar(16) DEFAULT NULL, title varchar(20) DEFAULT NULL, active boolean DEFAULT NULL, code varchar(6) DEFAULT NULL, name varchar(32) DEFAULT NULL, asset_tag varchar(16) DEFAULT NULL, description text DEFAULT NULL, asset_facility_name varchar(32) DEFAULT NULL, acquired timestamp NULL, disposed timestamp NULL DEFAULT NULL, trans_asset_tag varchar(16) DEFAULT NULL, requester_username varchar(16) DEFAULT NULL, request_time timestamp NULL, approver_username varchar(16) DEFAULT NULL, approval_time timestamp NULL, source_name varchar(32) DEFAULT NULL, destination_name varchar(32) DEFAULT NULL, load timestamp NULL, unload timestamp NULL)"
psql -d $1 -c "COPY temp (username, password, title, active) FROM '$VAR/users.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY temp (code, name) FROM '$VAR/facilities.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY temp (asset_tag, description, asset_facility_name, acquired, disposed) FROM '$VAR/assets.csv' WITH DELIMITER ',' CSV HEADER NULL AS 'NULL'"
psql -d $1 -c "COPY temp (trans_asset_tag, requester_username, request_time, approver_username, approval_time, source_name, destination_name, load, unload) FROM '$VAR/transfers.csv' DELIMITER ',' CSV HEADER"

psql -d $1 -c "INSERT INTO users (username, password, role_fk, active) SELECT username, password, 1, active FROM temp WHERE title='Logistics Officer' AND username IS NOT NULL"
psql -d $1 -c "INSERT INTO users (username, password, role_fk, active) SELECT username, password, 2, active FROM temp WHERE title='Facilities Officer' AND username IS NOT NULL"
psql -d $1 -c "INSERT INTO facilities (name, code) SELECT name, code FROM temp WHERE code IS NOT NULL"
psql -d $1 -c "INSERT INTO assets (asset_tag, description) SELECT asset_tag, description FROM temp WHERE asset_tag IS NOT NULL"
psql -d $1 -c "INSERT INTO asset_at (asset_fk, facility_fk, acquired, disposed) SELECT asset_id, facility_id, acquired, disposed FROM assets JOIN temp ON assets.asset_tag=temp.asset_tag JOIN facilities ON facilities.code=temp.asset_facility_name WHERE temp.asset_tag IS NOT NULL"
psql -d $1 -c "INSERT INTO trans_request (requester_id, request_time, source, destination, asset_fk, approver_id, approval_time, load, unload) SELECT requester.user_id, request_time, source.facility_id, destination.facility_id, asset_id, approver.user_id, approval_time, load, unload FROM temp JOIN users requester ON requester.username=temp.requester_username JOIN facilities source ON source.code=temp.source_name JOIN facilities destination ON destination.code=temp.destination_name JOIN assets ON assets.asset_tag=temp.trans_asset_tag JOIN users approver ON approver.username=temp.approver_username WHERE trans_asset_tag IS NOT NULL"


cd ../../import
