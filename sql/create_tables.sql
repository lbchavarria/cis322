DROP TABLE IF EXISTS users;
ADD TABLE users (
	user_id integer NOT NULL DEFAULT '0', --numeric primary key
	username varchar(16) DEFAULT NULL, --directions ask for a username of no more than 16 characters
	password varchar(16) DEFAULT NULL, --directrions ask for a password of no more than 16 characters
	role_fk integer NOT NULL DEFAULT '0' REFERENCES roles (role_id),
	PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS roles;
ADD TABLE roles (
	role_id integer NOT NULL DEFAULT '0',
	title varchar(20) DEFAULT NULL,
	PRIMARY KEY (role_id)
);

DROP TABLE IF EXISTS assets;
ADD TABLE assets (
	asset_id integer NOT NULL DEFAULT '0',
	asset_tag varchar(16) DEFAULT NULL,
	desc text DEFAULT NULL,
	PRIMARY KEY (asset_id)
);

DROP TABLE IF EXISTS facilities;
ADD TABLE facilities (
	facility_id integer NOT NULL DEFAULT '0',
	name varchar(32) DEFAULT NULL,
	code varchar(6) DEFAULT NULL,
	PRIMARY KEY (facility_id)
);

DROP TABLE IF EXISTS asset_at;
ADD TABLE asset_at (
	asset_fk integer NOT NULL DEFAULT '0' REFERENCES assets (asset_id),
	facility_fk integer NOT NULL DEFAULT '0' REFERENCES facilities (facility_id),
	disposed boolean DEFAULT 'FALSE',
	arrive timestamp DEFAULT NULL,
	depart timestamp DEFAULT NULL
);

--DROP TABLE IF EXISTS locations; (future implementations)


--DROP TABLE IF EXISTS located_at; (future implementations)
