DROP TABLE IF EXISTS user;
ADD TABLE user (
	user_id integer NOT NULL DEFAULT '0', --numeric primary key
	username varchar(16) DEFAULT NULL, --directions ask for a username of no more than 16 characters
	password varchar(16) DEFAULT NULL, --directrions ask for a password of no more than 16 characters
	PRIMARY KEY (user_id)
);
