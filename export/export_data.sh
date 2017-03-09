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
cd ../export/$2
psql -d $1 -A -F", " -c "SELECT username, password, title AS role, active FROM users JOIN roles ON users.role_fk=roles.role_id" > users.csv
psql -d $1 -A -F", " -c "SELECT code AS fcode, name AS common_name FROM facilities" > facilities.csv
psql -d $1 -A -F", " -c "SELECT asset_tag, description, name AS facility, acquired, disposed FROM assets JOIN asset_at ON assets.asset_id=asset_at.asset_fk JOIN facilities ON facilities.facility_id=asset_at.facility_fk" > assets.csv
psql -d $1 -A -F", " -c "SELECT asset_tag, requester.username AS request_by, request_time AS request_dt, approver.username AS approve_by, approval_time AS approve_dt, source.name AS source, destination.name AS destination, load AS load_dt, unload AS unload_dt FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN users requester ON requester.user_id=trans_request.requester_id JOIN users approver ON approver.user_id=trans_request.approver_id JOIN facilities source ON source.facility_id=trans_request.source JOIN facilities destination ON destination.facility_id=trans_request.destination" >transfers.csv

cd ..
