#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./import_data.sh <dbname> <imput dir>"
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
cd ../export/$2
psql -d $1 -c "COPY (SELECT username, password, title FROM users JOIN roles ON users.role_fk=roles.role_id) FROM 'users.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY (SELECT code, name FROM facilities) FROM 'facilities.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY (SELECT asset_tag, description, name, disposed FROM assets JOIN asset_at ON assets.asset_id=asset_at.asset_fk JOIN facilities ON facilities.facility_id=asset_at.facility_fk) FROM 'assets.csv' DELIMITER ',' CSV HEADER"
psql -d $1 -c "COPY (SELECT asset_tag, requester.username, request_time, approver.username, approval_time, source.name, destination.name, load, unload FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN users requester ON requester.user_id=trans_request.requester_id JOIN users approver ON approver.user_id=trans_request.approver_id JOIN facilities source ON source.facility_id=trans_request.source JOIN facilities destination ON destination.facility_id=trans_request.destination) FROM 'transfers.csv' DELIMITER ',' CSV HEADER"

cd ../../import
