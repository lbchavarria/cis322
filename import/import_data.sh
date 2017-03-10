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
psql -d $1 -c "CREATE TABLE temp (username varchar(16) DEFAULT NULL, password varchar(16) DEFAULT NULL, title varchar(20) DEFAULT NULL, active boolean DEFAULT NULL, code varchar(6) DEFAULT NULL, name varchar(32) DEFAULT NULL, asset_tag varchar(16) DEFAULT NULL, description text DEFAULT NULL, asset_facility_name varchar(32) DEFAULT NULL, acquired timestamp DEFAULT NULL, disposed timestamp DEFAULT NULL, trans_asset_tag varchar(16) DEFAULT NULL, requester_username varchar(16) DEFAULT NULL, request_time timestamp DEFAULT NULL, approver_username varchar(16) DEFAULT NULL, approval_time timestamp DEFAULT NULL, source_name varchar(32) DEFAULT NULL, destination_name varchar(32) DEFAULT NULL, load timestamp DEFAULT NULL, unload timestamp DEFAULT NULL)"
psql -d $1 -c "COPY temp (username, password, title, active) FROM '$VAR/users.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY temp (code, name) FROM '$VAR/facilities.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY temp (asset_tag, description, asset_facility_name, acquired, disposed) FROM '$VAR/assets.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY temp (trans_asset_tag, requester_username, request_time, approver_username, approval_time, source_name, destination_name, load, unload) FROM '$VAR/transfers.csv' DELIMITER ',' CSV HEADER"

psql -d $1 -c "INSERT INTO users (username, password, role_fk, active) SELECT username, password, 1, active FROM temp WHERE title='Logistics Officer'"
psql -d $1 -c "INSERT INTO users (username, password, role_fk, active) SELECT username, password, 2, active FROM temp WHERE title='Facilities Officer'"
psql -d $1 -c "INSERT INTO facilities (name, code) SELECT name, code FROM temp"
psql -d $1 -c "INSERT INTO assets (asset_tag, description) SELECT asset_tag, description FROM temp"
psql -d $1 -c "INSERT INTO asset_at (asset_fk, facility_fk, acquired, disposed) SELECT asset_id, facility_id, acquired, disposed FROM assets JOIN temp ON assets.asset_tag=temp.asset_tag JOIN facilities ON facilities.name=temp.asset_facility_name"
psql -d $1 -c "INSERT INTO trans_request (requester_id, request_time, source, destination, asset_fk, approver_id, approval_time, load, unload) SELECT requester.user_id, request_time, source.facility_id, destination.facility_id, asset_id, approver.user_id, approval_time, load, unload FROM temp JOIN users requester ON requester.username=temp.requester_username JOIN facilities source ON source.name=temp.source_name JOIN facilities destination ON destination.name=temp.destination_name JOIN assets ON assets.asset_tag=temp.trans_asset_tag JOIN users approver ON approver.username=temp.approver_username"

#psql -d $1 -c "COPY (SELECT username, password, title FROM users JOIN roles ON users.role_fk=roles.role_id) FROM 'users.csv' DELIMITER ',' CSV HEADER"
#psql -d $1 -c "COPY (SELECT code, name FROM facilities) FROM 'facilities.csv' DELIMITER ',' CSV HEADER"
#psql -d $1 -c "COPY (SELECT asset_tag, description, name, disposed FROM assets JOIN asset_at ON assets.asset_id=asset_at.asset_fk JOIN facilities ON facilities.facility_id=asset_at.facility_fk) FROM 'assets.csv' DELIMITER ',' CSV HEADER"
#psql -d $1 -c "COPY (SELECT asset_tag, requester.username, request_time, approver.username, approval_time, source.name, destination.name, load, unload FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN users requester ON requester.user_id=trans_request.requester_id JOIN users approver ON approver.user_id=trans_request.approver_id JOIN facilities source ON source.facility_id=trans_request.source JOIN facilities destination ON destination.facility_id=trans_request.destination) FROM 'transfers.csv' DELIMITER ',' CSV HEADER"

cd ../../import
