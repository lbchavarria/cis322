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
	PRIMARY KEY (user_id)
);

INSERT INTO roles VALUES
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
	disposed timestamp DEFAULT NULL,
	arrive timestamp DEFAULT NULL,
	depart timestamp DEFAULT NULL
);
