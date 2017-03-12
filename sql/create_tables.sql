DROP TABLE IF EXISTS roles CASCADE;
CREATE TABLE roles (
	role_id integer NOT NULL DEFAULT '0',
	title varchar(20) DEFAULT NULL,
	PRIMARY KEY (role_id)
);

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
	user_id serial, --numeric primary key
	username varchar(16) DEFAULT NULL, --directions ask for a username of no more than 16 characters
	password varchar(16) DEFAULT NULL, --directrions ask for a password of no more than 16 characters
	role_fk integer NOT NULL DEFAULT '0' REFERENCES roles (role_id),
	active boolean DEFAULT NULL,
	PRIMARY KEY (user_id)
);

INSERT INTO roles VALUES
	(0, ''),
	(1, 'Logistics Officer'),
	(2, 'Facilities Officer');

DROP TABLE IF EXISTS assets CASCADE;
CREATE TABLE assets (
	asset_id serial,
	asset_tag varchar(16) DEFAULT NULL,
	description text DEFAULT NULL,
	user_fk integer REFERENCES users(user_id),
	PRIMARY KEY (asset_id)
);

DROP TABLE IF EXISTS facilities CASCADE;
CREATE TABLE facilities (
	facility_id serial,
	name varchar(32) DEFAULT NULL,
	code varchar(6) DEFAULT NULL,
	user_fk integer REFERENCES users(user_id),
	PRIMARY KEY (facility_id)
);

DROP TABLE IF EXISTS asset_at CASCADE;
CREATE TABLE asset_at (
	asset_fk integer NOT NULL DEFAULT '0' REFERENCES assets (asset_id),
	facility_fk integer NOT NULL DEFAULT '0' REFERENCES facilities (facility_id),
	acquired timestamp NULL DEFAULT NULL,
	disposed timestamp NULL DEFAULT NULL,
	arrive timestamp NULL DEFAULT NULL,
	depart timestamp NULL DEFAULT NULL
);

DROP TABLE IF EXISTS trans_request CASCADE;
CREATE TABLE trans_request (
	transit_id serial,
	requester_id integer NOT NULL DEFAULT '0' REFERENCES users (user_id),
	request_time timestamp NULL DEFAULT NULL,
	source integer NOT NULL DEFAULT '0' REFERENCES facilities (facility_id),
	destination integer NOT NULL DEFAULT '0' REFERENCES facilities (facility_id),
	asset_fk integer NOT NULL DEFAULT '0' REFERENCES assets (asset_id),
	is_approved boolean,
	approver_id integer NOT NULL DEFAULT '0' REFERENCES users (user_id),
	approval_time timestamp NULL DEFAULT NULL,
	load timestamp NULL DEFAULT NULL,
	load_by integer REFERENCES users (user_id),
	unload timestamp NULL DEFAULT NULL,
	unload_by integer REFERENCES users (user_id),
	PRIMARY KEY (transit_id)
);

