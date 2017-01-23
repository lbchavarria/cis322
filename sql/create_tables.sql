CREATE DATABASE IF NOT EXISTS lost;
USE lost;

CREATE SCHEMA IF NOT EXISTS asset_tables;

DROP TABLE IF EXISTS asste_tables.products;
CREATE TABLE asset_tables.products (
	product_pk integer NOT NULL DEFAULT '0',
	vendor text DEFAULT NULL,
	description text DEFAULT NULL,
	alt_description text DEFAULT NULL,
	PRIMARY KEY (product_pk)
);

DROP TABLE IF EXISTS asset_tables.assets;
CREATE TABLE asset_tables.assets (
	asset_pk integer NOT NULL DEFAULT '0',
	product_fk integer NOT NULL DEFAULT '0',
	asset_tag text DEFAULT NULL,
	description text DEFAULt NULL,
	alt_description DEFAULT NULL,
	PRIMARY KEY (asset_pk),
	KEY product_fk1 (product_fk),
	CONSTRAINT product_fk1 FOREIGN KEY (product_fk) REFERENCES asset_tables.products (product_pk)
);

DROP TABLE IF EXISTS asset_tables.vehicle;
CREATE TABLE asset_tables.vehicles (
	vehicle_pk integer NOT NULL DEFAULT '0',
	asset_fk integer NOT NULL DEFAULT '0',
	PRIMARY KEY (vehicle_pk),
	KEY asset_fk1 (asset_fk),
	CONSTRAINT asset_fk1 FOREIGN KEY (asset_fk) REFERENCES asset_tables.assets (asset_pk)
);

DROP TABLE IF EXISTS asset_tables.facilities;
CREATE TABLE asset_tables.facilities (
	facility_pk integer NOT NULL DEFAULT '0',
	fcode text DEFAULT NULL,
	common_name text DEFAULT NULL,
	location text DEFAULT NULL,
	PRIMARY KEY (facility_pk)
);

DROP TABLE IF EXISTS asset_tables.asset_at;
CREATE TABLE asset_tables.asset_at (
	asset_fk integer NOT NULL DEFAULT '0',
	facility_fk integer NOT NULL DEFAULT '0',
	arrive_dt timestamp DEFAULT NULL,
	depart_dt timestamp DEFAULT NULL,
	KEY asset_fk2 (asset_fk),
	KEY facility_fk1 (facility_fk),
	CONSTRAINT asset_fk2 FOREIGN KEY (asset_fk) REFERENCES asset_tables.assets (asset_pk),
	CONSTRAINT facility_fk1 FOREIGN KEY (facility_fk) REFERENCES asset_tables.facilities (facility_pk)
);

DROP TABLE IF EXISTS asset_tables.convoys;
CREATE TABLE asset_tables.convoys (
	convoy_pk integer NOT NULL DEFAULT '0',
	request text DEFAULT NULL,
	source_fk integer NOT NULL DEFAULT '0',
	dest_fk integer NOT NULL DEFAULT '0',
	depart_dt timestamp DEFAULT NULL,
	arrive_dt timestamp DEFAULT NULL,
	PRIMARY KEY (convoy_pk),
	KEY source_fk1 (source_fk),
	KEY dest_fk1 (dest_fk),
	CONSTRAINT source_fk1 FOREIGN KEY (source_fk) REFERENCES asset_tables.facilities (facility_pk),
	CONSTRAINT dest_fk1 FOREIGN KEY (dest_fk) REFERENCES asset_tables.facilities (facility_pk)
);

DROP TABLE IF EXISTS asset_tables.used_by;
CREATE TABLE asset_tables.used_by (
	vehicle_fk integer NOT NULL DEFAULT '0',
	convoy_fk integer NOT NULL DEFAULT '0',
	KEY vehicle_fk1 (vehicle_fk),
	KET convoy_fk1 (convoy_fk)
	CONSTRAINT vehicle_fk1 FOREIGN KEY (vehicle_fk) REFERENCES asset_tables.vehicles (vehicle_pk),
	CONSTRAINT convoys_fk1 FOREIGN KEY (convoy_fk) REFERENCES asset_tables.convoys (convoy_pk)
);

DROP TABLE IF EXISTS asset_tables.asset_on;
CREATE TABLE asset_tables.asset_on (
	asset_fk integer NOT NULL DEFAULT '0',
	convoy_fk integer NOT NULL DEFAULT '0',
	load_dt timestamp DEFAULT NULL,
	unload_dt timestamp DEFAULT NULL,
	KEY asset_fk3 (asset_fk),
	KEY convoy_fk2 (convoy_fk),
	CONSTRAINT asset_fk3 FOREIGN KEY (asset_fk) REFERENCES asset_tables.assets (asset_pk),
	CONSTRAINT convoy_fk2 FOREIGN KEY (convoy_fk) REFERENCES asset_tables.convoys (convoy_pk)
);

CREATE SCHEMA IF NOT EXISTS user_tables;

DROP TABLE IF EXISTS user_tables.users;
CREATE TABLE user_tables.users (
	user_pk integer NOT NULL DEFAULT '0',
	username text DEFAULT NULL,
	active boolean DEFAULT NULL,
	PRIMARY KEY (user_pk)
);

DROP TABLE IF EXISTS user_tables.roles;
CREATE TABLE user_tables.roles (
	role_pk integer NOT NULL DEFAULT '0',
	title text DEFAULT NULL,
	PRIMRY KEY (role_pk)
);


