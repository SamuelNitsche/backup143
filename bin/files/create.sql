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

CREATE TABLE IF NOT EXISTS "143_emails" (
	id integer PRIMARY KEY AUTOINCREMENT,
	userid integer,
	email VARCHAR(255),
	value boolean
);

INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'login_notify', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'pool_created', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'pool_deleted', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'pool_changed', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'backup_started', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'backup_successful', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'backup_failed', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'backup_changed', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'backup_trojanercheck', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'restore_started', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'restore_successful', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'restore_failed', 1);
INSERT INTO "143_emails" (userid, email, value) VALUES (1, 'restore_changed', 1);

CREATE TABLE IF NOT EXISTS "143_options" (
	id integer PRIMARY KEY AUTOINCREMENT,
	option VARCHAR(255),
	value VARCHAR(255)
);

INSERT INTO "143_options" (option, value) VALUES ('smtp_server', 'localhost');
INSERT INTO "143_options" (option, value) VALUES ('smtp_port', '25');
INSERT INTO "143_options" (option, value) VALUES ('smtp_username', '');
INSERT INTO "143_options" (option, value) VALUES ('smtp_passwort', '');
INSERT INTO "143_options" (option, value) VALUES ('smtp_usessl', '');
INSERT INTO "143_options" (option, value) VALUES ('smtp_usetls', '');

CREATE TABLE IF NOT EXISTS "143_log" (
	id integer PRIMARY KEY AUTOINCREMENT,
	date datetime,
	type VARCHAR(255),
	relid integer,
	msg VARCHAR(255)
);

INSERT INTO "143_log" (date, type, relid, msg) VALUES (DATE(), 'user', 1, 'User "admin" successfully created');

CREATE TABLE IF NOT EXISTS "143_tasks" (
	id integer PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255),
	action VARCHAR(255),
	schedule integer,
	last_run datetime,
	planned_time datetime,
	status VARCHAR(255),
	backupid integer
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
	compression VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "143_permissions" (
	id integer PRIMARY KEY AUTOINCREMENT,
	userid integer,
	permission VARCHAR(255),
	value boolean
);

INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'access_home', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'access_pool', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'create_pool', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'modify_pool', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'delete_pool', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'access_backup', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'create_backup', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'modify_backup', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'delete_backup', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'access_resore', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'create_restore', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'modify_restore', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'delete_restore', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'access_settings', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'modify_settings_smtp', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'modify_settings_users', 1);
INSERT INTO "143_permissions" (userid, permission, value) VALUES (1, 'modify_settings_permissions', 1);

CREATE TABLE IF NOT EXISTS "143_tasklog" (
	id integer PRIMARY KEY AUTOINCREMENT,
	date datetime,
	taskid integer,
	value VARCHAR(255)
);

