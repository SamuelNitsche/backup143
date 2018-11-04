CREATE TABLE "143_users" (
	id integer PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(255),
	firstname VARCHAR(255),
	lastname VARCHAR(255),
	email VARCHAR(255),
	password binary,
	last_login datetime,
	active boolean
);

INSERT INTO "143_users" (id, username, firstname, lastname, email, password, last_login, active) VALUES (1, 'admin', 'Firstname', 'Lastname', 'admin@backup143.py', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec', '00-00-0000', 1);

CREATE TABLE IF NOT EXISTS "143_pwreset" (
	id integer PRIMARY KEY AUTOINCREMENT,
	userid integer,
	authcode VARCHAR(255),
    req_date datetime
);

CREATE TABLE IF NOT EXISTS "143_options" (
	id integer PRIMARY KEY AUTOINCREMENT,
	option VARCHAR(255),
	value VARCHAR(255)
);

INSERT INTO "143_options" (option, value) VALUES ('smtp_server', 'localhost');
INSERT INTO "143_options" (option, value) VALUES ('smtp_port', '25');
INSERT INTO "143_options" (option, value) VALUES ('smtp_username', '');
INSERT INTO "143_options" (option, value) VALUES ('smtp_password', '');
INSERT INTO "143_options" (option, value) VALUES ('smtp_usessl', '');
INSERT INTO "143_options" (option, value) VALUES ('smtp_usetls', '');

CREATE TABLE IF NOT EXISTS "143_tasks" (
	id integer PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255),
	action VARCHAR(255),
	schedule VARCHAR(255),
	last_run VARCHAR(255),
	state VARCHAR(255),
	backupid integer,
	backuptyp VARCHAR(255),
    backupfilesid integer
);

CREATE TABLE IF NOT EXISTS "143_pool" (
	id integer PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255),
	system VARCHAR(255),
	host VARCHAR(255),
	port integer,
	username binary,
	password binary,
	path VARCHAR(255),
	ownerid integer
);

CREATE TABLE IF NOT EXISTS "143_sessions" (
	id integer PRIMARY KEY AUTOINCREMENT,
	hash binary,
	userid integer
);

CREATE TABLE IF NOT EXISTS "143_backups" (
	id integer PRIMARY KEY AUTOINCREMENT,
	pool_src integer,
	pool_dst integer,
	compare VARCHAR(255),
	encrypt boolean,
	compression VARCHAR(255),
	last_full_run datetime
);

CREATE TABLE IF NOT EXISTS "143_tasklog" (
	id integer PRIMARY KEY AUTOINCREMENT,
	date datetime,
	taskid integer,
	value VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "143_backupfiles" (
	id integer PRIMARY KEY AUTOINCREMENT,
	date datetime,
	taskid integer,
	state VARCHAR(255),
	path VARCHAR(255)
);